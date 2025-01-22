import pytest
from server import app
from datetime import datetime, timedelta

@pytest.fixture
def client():
    """
    Crée un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_data(monkeypatch):
    """
    Remplace les données de compétitions et de clubs par des valeurs fictives.
    """

    # Création de compétitions fictives
    test_competitions = [
        {"name": "Past Competition", "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), "numberOfPlaces": "10"},
        {"name": "Future Competition", "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), "numberOfPlaces": "10"}
    ]

    # Création de clubs fictifs
    test_clubs = [
        {"name": "Elite Club", "points": "15"}
    ]

    # Monkeypatch pour utiliser ces données au lieu de celles du JSON
    monkeypatch.setattr("server.competitions", test_competitions)
    monkeypatch.setattr("server.clubs", test_clubs)

def test_booking_past_competition(client, mock_data):
    """
    Vérifie qu'on ne peut pas réserver une compétition déjà passée.
    """
    response = client.post('/purchasePlaces', data={
        'competition': 'Past Competition',
        'club': 'Elite Club',
        'places': 3
    })
    assert b"You cannot book places for a past competition." in response.data

def test_booking_future_competition(client, mock_data):
    """
    Vérifie qu'on peut réserver une compétition future.
    """
    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition',
        'club': 'Elite Club',
        'places': 3
    })
    assert b"Great-booking complete!" in response.data
