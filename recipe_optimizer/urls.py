from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='optimize'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='optimize_recipe'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),

]
