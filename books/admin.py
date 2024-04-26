from django.contrib import admin

# Register your models here.
from .models import Book, Category, Review

admin.site.register(Book)

admin.site.register(Review)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Category, CategoryAdmin)    