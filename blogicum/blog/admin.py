from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

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

    @admin.display(description='Изображение')
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="/%s" width="150" height="150" />' % obj.image
            )
        else:
            return "Нет изображения"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.with_comment_count()
    
    @admin.display(description='Количество комментариев')
    def get_comment_count(self, obj):
        return obj.comment_count

    common_list = (
        'title',
        'is_published',
        'pub_date',
        'author',
        'category',
        'location',
        'text',
        'image',
    )
    list_display = (
        ('__str__',)
        + common_list
        + ('image_tag',)
        + ('get_comment_count',)
    )
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
