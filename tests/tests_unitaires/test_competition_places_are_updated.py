import pytest
import json
from server import app, loadCompetitions, saveCompetitions

@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_competitions(monkeypatch):
    """
    Charge les compétitions depuis le fichier JSON et empêche l'écriture réelle.
    """
    with open('competitions.json') as f:
        test_competitions = json.load(f)['competitions']

    # Monkeypatch pour utiliser ces compétitions en mémoire
    monkeypatch.setattr("server.competitions", test_competitions)

    # Monkeypatch pour empêcher l'écriture sur le fichier JSON
    monkeypatch.setattr("server.saveCompetitions", lambda competitions: None)

    return test_competitions  # Retourne les compétitions simulées

def test_competition_places_are_updated(client, mock_competitions):
    """
    Vérifie que le nombre de places d'une compétition est mis à jour après une réservation,
    sans modifier le fichier competitions.json.
    """
    competition_name = "Spring Festival"
    initial_places = int(next(c for c in mock_competitions if c['name'] == competition_name)['numberOfPlaces'])

    # Simuler une réservation de 5 places
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': 'Simply Lift',
        'places': 5
    })

    # Vérifier si les places ont été mises à jour en mémoire
    updated_places = int(next(c for c in mock_competitions if c['name'] == competition_name)['numberOfPlaces'])

    # Vérifications
    assert updated_places == initial_places - 5, f"Expected {initial_places - 5}, got {updated_places}"
    assert b"Great-booking complete!" in response.data  # Vérifier le message de confirmation
