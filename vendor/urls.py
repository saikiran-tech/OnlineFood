from django.urls import path, include
from . import views
from foodapp import views as accountViews
urlpatterns = [
    # path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name='v_profile'),
    path('menu-builder/', views.menu_builder, name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    #add category
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category')


]