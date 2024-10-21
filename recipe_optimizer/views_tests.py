import pytest
from django.urls import reverse
from django.test import Client
from .models import Recipe, RecipeStep


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def sample_recipe(db):
    # Örnek bir tarif oluşturuyoruz
    recipe = Recipe.objects.create(
        name="Test Recipe",
        description="This is a test recipe."
    )
    return recipe


@pytest.fixture
def sample_step(db, sample_recipe):
    # Örnek bir adım oluşturuyoruz
    step = RecipeStep.objects.create(
        recipe=sample_recipe,
        name="Test Step",
        duration=30,
        occupies_chef=True
    )
    return step


def test_index_view(client, sample_recipe):
    """index view testi - tariflerin listelenmesi"""
    url = reverse('index')
    response = client.get(url)

    # HTTP 200 dönmesi gerekiyor
    assert response.status_code == 200
    # Tarifi içerdiğinden emin olun
    assert sample_recipe.name in response.content.decode()


def test_create_recipe_view(client, db):
    """create_recipe view testi - tarif oluşturma"""
    url = reverse('create_recipe')
    data = {
        'name': 'New Recipe',
        'description': 'This is a new recipe.'
    }
    response = client.post(url, data)

    # HTTP 302 dönmesi (redirect) gerekiyor
    assert response.status_code == 302

    # Tarifin başarıyla oluşturulup oluşturulmadığını kontrol et
    assert Recipe.objects.filter(name="New Recipe").exists()


def test_optimize_recipe_view(client, sample_recipe, sample_step):
    """optimize_recipe view testi - adımların optimize edilmesi"""
    url = reverse('optimize_recipe', args=[sample_recipe.id])
    response = client.get(url)

    # HTTP 200 dönmesi gerekiyor
    assert response.status_code == 200
    # Adımın sayfada yer aldığından emin olun
    assert sample_step.name in response.content.decode()


def test_delete_recipe_view(client, sample_recipe):
    """delete_recipe view testi - tarifin silinmesi"""
    url = reverse('delete_recipe', args=[sample_recipe.id])
    response = client.post(url)

    # HTTP 302 dönmesi (redirect) gerekiyor
    assert response.status_code == 302

    # Tarifin silindiğinden emin olun
    assert not Recipe.objects.filter(id=sample_recipe.id).exists()


def test_recipe_json_view(client, sample_recipe, sample_step):
    """recipe_json view testi - JSON yanıtı"""
    url = reverse('recipe_json', args=[sample_recipe.id])
    response = client.get(url)

    # HTTP 200 dönmesi gerekiyor ve application/json tipi olmalı
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    # JSON verisi içeriğini kontrol edelim
    json_data = response.json()
    assert json_data['recipe']['name'] == sample_recipe.name
    assert json_data['recipe']['steps'][0]['name'] == sample_step.name
