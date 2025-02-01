import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True  # Active le mode test de Flask
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_save_clubs(monkeypatch):
    """Empêche la sauvegarde des clubs dans clubs.json lors des tests."""
    monkeypatch.setattr("server.save_club_points_db", lambda clubs, file_path="clubs.json": None)



def test_purchase_more_places_than_available(client):
    """
    Teste qu'un club ne peut pas acheter plus de places que de places disponibles.
    """

    # Charger dynamiquement le JSON clubs.json
    clubs = loadClubs()
    comeptitions = loadCompetitions()

    # Simuler une réservation avec plus de points que disponibles
    response = client.post('/purchasePlaces', data={
        'competition': comeptitions[0]['name'],
        'club': clubs[0]['name'],
        'places': int(comeptitions[0]['numberOfPlaces']) + 1  # Réserver plus que de places disponibles
    })

    # Vérifie que l'utilisateur est redirigé vers la page de résumé (code 200)
    assert response.status_code == 200
    
    # Vérifier que l'utilisateur reçoit un message d'erreur
    assert b"You can not book more places than availables" in response.data


