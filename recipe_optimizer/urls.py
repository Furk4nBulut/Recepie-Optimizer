from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipes_list, name='recipes_list'),
    path('recipes/add/', views.add_new_recipe, name='add_new_recipe'),
    path('recipes/optimize/', views.optimize_recipe, name='optimize_recipe'),
]
