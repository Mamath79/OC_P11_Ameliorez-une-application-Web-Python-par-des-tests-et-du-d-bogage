import pytest
from server import app, loadClubs


@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_purchase_more_places_than_points(client):
    """
    Teste qu'un club ne peut pas acheter plus de 12 places.
    """

    # Charger dynamiquement le JSON clubs.json
    clubs = loadClubs()
    
    # Prendre le premier club et récupérer son nombre de points
    club_name = clubs[0]['name']

    # Simuler une réservation avec plus de points que disponibles
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': 13  # Réserver plus que les points disponibles
    })

    # Vérifie que l'utilisateur est redirigé vers la page de résumé (code 200)
    assert response.status_code == 200
    
    # Vérifier que l'utilisateur reçoit un message d'erreur
    assert b"You can not book more than 12 places." in response.data


def test_purchase_exactly_twelve_places(client):
    """
    Teste qu'un club peut réserver exactement 12 places sans problème.
    """
    
    # Charger dynamiquement le JSON clubs.json
    clubs = loadClubs()
    
    # Prendre le premier club et récupérer son nombre de points
    club_name = clubs[0]['name']

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': club_name,
        'places': 12
    })
    
    # Vérifie que l'utilisateur est redirigé vers la page de résumé (code 200)
    assert response.status_code == 200
    
    assert b"Great-booking complete!" in response.data
    