from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Location, Post

admin.site.unregister(Group)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    common_list = (
        'is_published',
        'name',
    )
    list_display = ('__str__',) + common_list
    list_editable = common_list


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    common_list = (
        'title',
        'is_published',
        'pub_date',
        'author',
        'category',
        'location',
        'text',
        'image'
    )
    list_display = ('__str__',) + common_list + ('image_tag',) + ('comment_count',)
    list_editable = common_list


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    common_list = (
        'is_published',
        'description',
        'slug'
    )
    list_display = ('__str__', ) + common_list
    list_editable = common_list


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    common_list = (
        'text',
        'created_at',
        'author'
    )
    list_display = ('__str__', ) + common_list
