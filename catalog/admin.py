from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('cake_name', 'slug', 'price', 'category', 'size')
    list_filter = ('cake_name', 'price', 'category', 'size')
    list_editable = ('price', 'size')
    prepopulated_fields = {'slug': ('cake_name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'review')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject')
