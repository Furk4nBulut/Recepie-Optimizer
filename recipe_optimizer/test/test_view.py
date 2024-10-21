import pytest
from django.urls import reverse
from django.test import Client
from recipe_optimizer.models import Recipe, RecipeStep


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def sample_recipe(db):
    recipe = Recipe.objects.create(
        name="Test Recipe",
        description="This is a test recipe."
    )
    return recipe


@pytest.fixture
def sample_step(db, sample_recipe):
    step = RecipeStep.objects.create(
        recipe=sample_recipe,
        name="Test Step",
        duration=30,
        occupies_chef=True
    )
    return step


def test_index_view(client, sample_recipe):
    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200
    assert sample_recipe.name in response.content.decode()


def test_create_recipe_view(client, db):
    url = reverse('create_recipe')
    data = {
        'name': 'New Recipe',
        'description': 'This is a new recipe.'
    }
    response = client.post(url, data)

    assert response.status_code == 302

    assert Recipe.objects.filter(name="New Recipe").exists()


def test_optimize_recipe_view(client, sample_recipe, sample_step):
    """optimize_recipe view testi - adımların optimize edilmesi"""
    url = reverse('optimize_recipe', args=[sample_recipe.id])
    response = client.get(url)

    assert response.status_code == 200

    assert sample_step.name in response.content.decode()


def test_delete_recipe_view(client, sample_recipe):
    url = reverse('delete_recipe', args=[sample_recipe.id])
    response = client.post(url)

    assert response.status_code == 302

    assert not Recipe.objects.filter(id=sample_recipe.id).exists()


def test_recipe_json_view(client, sample_recipe, sample_step):
    url = reverse('recipe_json', args=[sample_recipe.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    json_data = response.json()
    assert json_data['recipe']['name'] == sample_recipe.name
    assert json_data['recipe']['steps'][0]['name'] == sample_step.name
