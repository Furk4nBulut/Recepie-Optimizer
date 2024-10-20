from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='optimize'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='optimize_recipe'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),
    path('edit-step/<int:recipe_id>/<int:step_id>/', views.edit_step, name='edit_step'),
    path('delete-step/<int:recipe_id>/<int:step_id>/', views.delete_step, name='delete_step'),
    path('recipe/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe-json/<int:recipe_id>/', views.recipe_json, name='recipe_json'),
]
