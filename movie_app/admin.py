from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Category, Movies, Review


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'poster', 'category', 'available', 'release_date', 'youtube_link','actors','user'











                    ]
    list_editable = [ 'available']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


admin.site.register(Movies, MovieAdmin)
admin.site.register(Review)

