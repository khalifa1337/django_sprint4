from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post

admin.site.unregister(Group)


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
        'text'
    )
    list_display = ('__str__',) + common_list
    list_editable = common_list


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    common_list = (
        'is_published',
        'description',
        'slug'
    )
    list_display = ('__str__', ) + common_list
    list_editable = common_list
