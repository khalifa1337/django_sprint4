from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.list import MultipleObjectMixin

from core.constants import ELEMENTS_TO_SHOW

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

"""
Так как в данном файле используются, в большинстве своем, базовые
классы, то аннотация типов не использовалась.
"""

User = get_user_model()
"""
Получение модели пользователя для дальнейшего использования.
Так как по тексту задания и потребности в целом не было
необходимости, то используется базовая модель.
Хотя, возможно, её стоило, согласно рекомендациям,
перелпоежедить изначально.
"""


class OnlyAuthorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Миксин для проверки принадлежости поста автору.
    Включает проверку на авторизацию на сайте (LoginReqiuerMixin).
    """

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id


class PostMixin:
    """Миксин для CBV, связанных с моделью и формой Post."""

    model = Post
    form_class = PostForm


class CommentMixin:
    """Миксин для CBV, связанных с моделью и формой Post."""

    model = Comment
    form_class = CommentForm


class CachedObjectMixin:
    """Миксин для кеширования данных."""

    def get_object(self, queryset=None):
        """
        При попытке оптимизации количества SQL запросов было замечено, что
        основной запрос на загрузку данных дублировался. Данное решение помогло
        избежать дублирования. (Не уверен, что данный подход на 100% оправдан)
        """
        if not hasattr(self, '_cached_object'):
            self._cached_object = super().get_object(queryset)
        return self._cached_object


class Index(ListView):
    """CBV для отображения постов на главной странице."""

    model = Post
    queryset = (
        Post
        .published
        .with_comment_count()
        .select_related('author', 'category', 'location')
    )
    paginate_by = ELEMENTS_TO_SHOW


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    """CBV для формы создания поста."""

    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(CachedObjectMixin, DetailView):
    """CBV для получения подробной информации о посте."""

    model = Post
    queryset = Post.objects.select_related('author', 'location', 'category')
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        """
        Переопределение метода get_object для проверки публикации
        и авторства поста.
        """
        obj = super().get_object(queryset)
        if not obj.is_published and obj.author != self.request.user:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        """Добавление имеющихся комментариев на страницу публикации."""
        context = dict(
            **super().get_context_data(**kwargs),
            form=CommentForm(),
            comments=self.object.comment.select_related('author')
        )
        return context


class PostUpdateView(PostMixin, OnlyAuthorMixin, UpdateView):
    """CBV для редактирования поста."""

    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        """
        Принудительный редирект пользователя на страницу поста в случае попытки
        его редактирования не автором.
        """
        return (
            HttpResponseRedirect(
                reverse(
                    'blog:post_detail',
                    kwargs={self.pk_url_kwarg: self.kwargs[self.pk_url_kwarg]}
                )
            )
        )

    def get_success_url(self):
        """
        Возможно, есть смысл как-то объединить с функцией выше, но, если я
        верно понимаю, логика вызовов разная. Из вариантов - вынести в другую
        функцию reverse, но по количеству кода выигрыша не будет.
        """
        return reverse(
            'blog:post_detail',
            kwargs={self.pk_url_kwarg: self.kwargs[self.pk_url_kwarg]}
        )


class PostDeleteView(CachedObjectMixin, OnlyAuthorMixin, DeleteView):
    """CBV для удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')


class CategoryListView(CachedObjectMixin, DetailView, MultipleObjectMixin):
    """CBV для отображения странциы отдельной категории"""

    slug_url_kwarg = 'post_id'
    model = Category
    context_object_name = 'category'
    paginate_by = ELEMENTS_TO_SHOW

    def get_object(self, queryset=None):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True)

    def get_queryset(self):
        return (
            Post
            .published
            .with_comment_count()
            .select_related('author', 'category', 'location')
            .filter(category__slug=self.kwargs['category_slug'])
        )

    def get_context_data(self, **kwargs):
        """
        Если посмотреть по дебагу, то запрос частично дублируется.
        Вернее, там вызывается count из-за, как я понимаю, annotate,
        но я не знаю, можно ли объединить в один запрос
        """
        context = super().get_context_data(
            object_list=self.get_queryset(),
            **kwargs
        )
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    """CBV для формы написания комментария."""

    comment_post = None

    def dispatch(self, request, *args, **kwargs):
        self.comment_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment_post = self.comment_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.comment_post.pk}
        )


class CommentUpdateView(
    CommentMixin,
    CachedObjectMixin,
    OnlyAuthorMixin,
    UpdateView
):
    """CBV для изменения комментария"""

    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        post_id = self.object.comment_post.id
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': post_id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    """CBV для удаления комментария."""

    template_name = 'blog/comment_form.html'
    pk_url_kwarg = 'comment_id'

    def get_object(self, queryset=None):
        """
        Так как в запросе поступает два ключа, то производим переопределение
        функции обработки. Возможно, что есть более лаконичное решение.
        """
        post = self.kwargs['post_id']
        comment = self.kwargs[self.pk_url_kwarg]
        obj = get_object_or_404(Comment, comment_post=post, id=comment)
        return obj

    def get_success_url(self):
        return (
            reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs['post_id']})
        )


class UserProfileView(DetailView, MultipleObjectMixin):
    """CBV дял отображения профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = ELEMENTS_TO_SHOW

    def get_context_data(self, **kwargs):
        profile_user = self.object
        current_user = self.request.user
        filter_condition = Q(author=profile_user)
        if profile_user != current_user:
            filter_condition &= Q(
                is_published=True,
                pub_date__lte=timezone.now())
        """Так как автор постов должен их видеть, то добавляем условие выше."""
        object_list = (
            Post
            .objects
            .filter(filter_condition)
            .with_comment_count()
            .select_related('author', 'category', 'location')
            .ordered_by_pub_date()
        )
        """
        Так как список не всегда идентичен тому, что используется на других
        страницах, то, если я правильно понимаю, имеющийся менеджер
        тут может не подойти.
        """
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для страницы имзенения информации о пользователе."""

    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return (
            reverse(
                'blog:profile',
                kwargs={'username': self.request.user.username}
            )
        )
