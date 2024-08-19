from django.urls import path
from . import views

urlpatterns = [
    path('categorylist/', views.get_categories, name='category-list'),
    path('subcategorylist/', views.get_subcategories, name='subcategory-list'),
]
