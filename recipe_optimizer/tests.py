import pytest
from django.test import Client
from .models import Recipe, Step

@pytest.mark.django_db
def test_add_recipe():
    client = Client()
    response = client.post('/add_recipe/', {
        'name': 'Chocolate Chip Cookies',
        'description': 'A classic recipe',
        'total_time': 120,
        'steps-TOTAL_FORMS': 1,
        'steps-INITIAL_FORMS': 0,
        'steps-MIN_NUM_FORMS': 0,
        'steps-MAX_NUM_FORMS': 1000,
        'steps-0-description': 'Mix dry ingredients',
        'steps-0-duration': 10,
        'steps-0-occupies_chef': True,
    })
    assert response.status_code == 302
    assert Recipe.objects.count() == 1
    assert Step.objects.count() == 1
