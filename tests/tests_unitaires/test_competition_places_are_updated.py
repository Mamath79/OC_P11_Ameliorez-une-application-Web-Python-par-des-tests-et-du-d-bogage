import pytest
import json
from server import app, loadCompetitions, saveCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_competition_places_are_updated(client, monkeypatch):
    """
    Vérifie que le nombre de places d'une compétition est mis à jour après une réservation,
    sans modifier le fichier competitions.json.
    """

    # Charger et cloner les données actuelles de competitions.json
    with open('competitions.json') as f:
        competitions_data = json.load(f)['competitions']

    # Monkeypatch pour utiliser le clone au lieu des données globales
    monkeypatch.setattr("server.competitions", competitions_data)

    # Monkeypatch : Empêcher l'écriture dans le fichier JSON
    monkeypatch.setattr("server.saveCompetitions", lambda competitions: None)

    # Charger les compétitions (depuis la mémoire simulée)
    competition_name = "Spring Festival"
    initial_places = int(next(c for c in competitions_data if c['name'] == competition_name)['numberOfPlaces'])

    # Simuler une réservation de 5 places
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': 'Simply Lift',
        'places': 5
    })

    # Vérifier si les places ont été mises à jour
    updated_places = int(next(c for c in competitions_data if c['name'] == competition_name)['numberOfPlaces'])

    # Assertions
    assert updated_places == initial_places - 5
    assert b'Great-booking complete!'in response.data  # Vérifier le message de confirmation
