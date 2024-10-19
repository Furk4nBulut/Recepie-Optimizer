from django.urls import path
from . import views

urlpatterns = [
    path('', views.optimize_recipe, name='optimize_recipe'),
]
