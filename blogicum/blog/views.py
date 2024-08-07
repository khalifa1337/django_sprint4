
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from core.constants import ELEMENTS_TO_SHOW

from .forms import PostForm, CommentForm
from .models import Category, Post, Comment

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author_id == self.request.user.id


class Index(ListView):
    model = Post
    ordering = '-pub_date'
    queryset = Post.published.select_related('author', 'category').annotate(comment_count=Count('comment'))
    paginate_by = ELEMENTS_TO_SHOW



class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['comments'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.comment.select_related('author')
        )
        print(context)
        return context


class CategoryListView(DetailView, MultipleObjectMixin):
    model = Category
    # context_object_name = 'post_list'
    context_object_name = 'category'
    paginate_by = ELEMENTS_TO_SHOW

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(category=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        print(context)
        return context


class UserProfileView(DetailView, MultipleObjectMixin):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = ELEMENTS_TO_SHOW  # Количество постов на странице

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(author=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    comment_post = None
    model = Comment
    form_class = CommentForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.comment_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.comment_post = self.comment_post
        return super().form_valid(form)
    # Переопределяем get_success_url()

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.comment_post.pk})


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    # template_name = 'your_template_name.html'  # Replace with the name of your template

    def get_success_url(self):
        post_id = self.object.comment_post.id
        return reverse_lazy('blog:post_detail', kwargs={'pk': post_id})  # Update the view name and kwargs as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    
class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    def get_object(self, queryset=None):
        post = self.kwargs['post_id']
        comment = self.kwargs['comment_id']
        obj = get_object_or_404(Comment, comment_post=post, id=comment)
        return obj

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})
    
    
def UserProfileEdit():
    pass