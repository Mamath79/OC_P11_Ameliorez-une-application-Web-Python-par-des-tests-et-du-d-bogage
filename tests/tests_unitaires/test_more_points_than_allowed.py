import pytest
from server import app, loadClubs

@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True  # Active le mode test de Flask
    with app.test_client() as client:
        yield client


def test_purchase_more_places_than_points(client):
    """
    Teste qu'un club ne peut pas acheter plus de places qu'il n'a de points.
    """

    # Charger dynamiquement le JSON clubs.json
    clubs = loadClubs()
    
    # Prendre le premier club et récupérer son nombre de points
    club_name = clubs[0]['name']
    club_points = int(clubs[0]['points'])  

    # Simuler une réservation avec plus de points que disponibles
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': club_points + 1  # Réserver plus que les points disponibles
    })

    # Vérifier que l'utilisateur reçoit un message d'erreur
    assert b"You cannot book more places than your points allow." in response.data


def test_purchase_with_sufficient_points(client):
    """
    Teste qu'un club peut acheter des places tant qu'il a assez de points.
    """

    # Charger dynamiquement le JSON clubs.json
    clubs = loadClubs()
    
    # Prendre le premier club et récupérer son nombre de points
    club_name = clubs[0]['name']
    club_points = int(clubs[0]['points'])  

    # Vérifier qu'on peut acheter un nombre de places correct
    places_to_book = min(1, club_points)  # Assure que l'on prend au moins 1 place si possible
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': places_to_book
    })

    # Vérifier que la réservation réussit
    assert b"Great-booking complete!" in response.data
