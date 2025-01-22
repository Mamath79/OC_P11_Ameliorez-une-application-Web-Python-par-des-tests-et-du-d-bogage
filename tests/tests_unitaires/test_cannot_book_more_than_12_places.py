import pytest
from server import app

@pytest.fixture
def client():
    """Configure un client de test Flask pour simuler des requêtes HTTP."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_data(monkeypatch):
    """Remplace les données des compétitions et des clubs pour s'assurer que les tests fonctionnent."""
    
    # Données fictives mais réalistes
    test_clubs = [
        {"name": "Elite Club", "points": "15"},
        {"name": "Iron Temple", "points": "10"},
    ]
    
    test_competitions = [
        {"name": "Fictional Cup", "date": "2025-06-30 10:00:00", "numberOfPlaces": "30"}
    ]
    
    # Monkeypatch pour charger ces données à la place du JSON
    monkeypatch.setattr("server.clubs", test_clubs)
    monkeypatch.setattr("server.competitions", test_competitions)

def test_purchase_more_than_twelve_places(client, mock_data):
    """Teste qu'un club ne peut pas réserver plus de 12 places."""
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Fictional Cup',
        'club': 'Elite Club',
        'places': 13  # Plus de 12 places
    })
    
    assert b"You can not book more than 12 places." in response.data

def test_purchase_exactly_twelve_places(client, mock_data):
    """Teste qu'un club peut réserver exactement 12 places sans problème."""
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Fictional Cup',
        'club': 'Elite Club',
        'places': 12  # Limite maximale autorisée
    })
    
    assert b"Great-booking complete!" in response.data
