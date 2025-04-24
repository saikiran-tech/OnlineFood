from django.contrib import admin
from .models import Category, Fooditem
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')

class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('category', 'food_title', 'price', 'vendor')
    search_fields = ('category__categoty_name', 'vendor__vendor_name', 'food_title')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Fooditem, FooditemAdmin)