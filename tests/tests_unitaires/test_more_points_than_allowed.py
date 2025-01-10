import pytest
from server import app


@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True  # Active le mode test de Flask
    with app.test_client() as client:
        yield client


def test_purchase_more_places_than_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 20  # Plus que les points disponibles du club
    })
    assert b"You cannot book more places than your points allow." in response.data


