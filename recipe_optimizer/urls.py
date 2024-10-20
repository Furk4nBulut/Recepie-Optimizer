from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='optimize'),
    path('optimize/<int:recipe_id>/', views.optimize_recipe, name='add_recipe_step'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/list/', views.recipe_list, name='recipe_list'),  # Yeni tarif listesi yolu

]
