import pytest
import json
from server import app


@pytest.fixture
def client():
    """Crée un client de test Flask pour simuler des requêtes HTTP."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_data(monkeypatch):
    """
    Charge les données des clubs et empêche l'écriture sur le fichier JSON.
    """
    with open('clubs.json') as f:
        test_clubs = json.load(f)['clubs']

    # Monkeypatch pour charger les clubs depuis la copie
    monkeypatch.setattr("server.clubs", test_clubs)

    # Monkeypatch pour empêcher l'écriture dans clubs.json
    monkeypatch.setattr("server.save_club_points_db", lambda clubs: None)

    return test_clubs

def test_club_points_are_updated(client, mock_data):
    """
    Vérifie que les points d'un club sont bien mis à jour après un achat.
    """
    club_name = "Simply Lift"
    initial_points = int(next(c for c in mock_data if c['name'] == club_name)['points'])

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': 3
    })

    updated_points = int(next(c for c in mock_data if c['name'] == club_name)['points'])

    assert updated_points == initial_points - 3
    assert b"Great! Booking complete" in response.data
