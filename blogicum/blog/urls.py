from django.urls import include, path

from . import views

app_name = 'blog'

post_links = [
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        '<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        '<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
]

profile_links = [
    path(
        '<str:username>/',
        views.UserProfileView.as_view(),
        name='profile'
    ),
    path(
        'edit',
        views.UserUpdateView.as_view(),
        name='edit_profile'
    ),
]

category_links = [
    path(
        '<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
]

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index'
    ),
    path('posts/', include(post_links)),
    path('profile/', include(profile_links)),
    path('category/', include(category_links)),
]
