import pytest
import json
import copy
from server import app, loadClubs, loadCompetitions, saveClubs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_club_points_are_updated(client, monkeypatch):
    """
    Vérifie que les points du club sont mis à jour après une réservation,
    sans modifier le fichier clubs.json.
    """

    # Charger les données actuelles du JSON et les cloner
    test_clubs = copy.deepcopy(loadClubs())
    test_competitions = copy.deepcopy(loadCompetitions())

    # Monkeypatch : Remplacer les fonctions pour empêcher la lecture/écriture des fichiers
    monkeypatch.setattr("server.loadClubs", lambda: test_clubs)
    monkeypatch.setattr("server.loadCompetitions", lambda: test_competitions)
    monkeypatch.setattr("server.saveClubs", lambda clubs: None)  # Empêche la sauvegarde réelle

    # Monkeypatch : Mettre à jour les variables globales de Flask
    from server import clubs, competitions
    monkeypatch.setattr("server.clubs", test_clubs)
    monkeypatch.setattr("server.competitions", test_competitions)

    # Sélectionner un club et ses points
    club_name = "Simply Lift"
    initial_points = int(next(c for c in test_clubs if c['name'] == club_name)['points'])

    # Simuler l'achat de 3 places
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': 3
    })

    # Vérifier si les points ont été mis à jour dans la mémoire (sans affecter le JSON réel)
    updated_points = int(next(c for c in test_clubs if c['name'] == club_name)['points'])

    # Vérifier que la mise à jour est correcte
    assert updated_points == initial_points - 3
    assert b"Great! Booking complete" in response.data  # Vérifier le message de confirmation
