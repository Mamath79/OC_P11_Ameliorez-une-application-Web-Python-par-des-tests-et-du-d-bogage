import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app


@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config['TESTING'] = True  # Active le mode test de Flask
    with app.test_client() as client:
        yield client

def test_access_show_summary_with_invalid_email(client):
    """
    Teste que l'application gère correctement un e-mail inconnu en renvoyant une redirection
    et en affichant un message flash approprié.
    """
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})

    # Vérifie que l'utilisateur est redirigé (code 302)
    assert response.status_code == 302

    # Vérifie que le message flash "sorry, email not found" est présent
    with client.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any("sorry, email not found" in message[1] for message in flashed_messages)

def test_purchase_more_places_than_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 20  # Plus que les points disponibles du club
    })
    assert b"You cannot book more places than your points allow." in response.data


def test_purchase_more_places_than_available(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 300  # Plus que le nombre de places disponibles
    })
    assert b"Not enough places available in the competition." in response.data


def test_successful_purchase(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 2  # Réservation correcte
    })
    assert b"Great! Booking complete." in response.data


def test_purchase_zero_or_negative_places(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 0  # Réservation de zéro place
    })
    assert b"Invalid number of places." in response.data

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': -1  # Réservation d'un nombre négatif
    })
    assert b"Invalid number of places." in response.data


def test_purchase_with_invalid_club_or_competition(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Non-existent Competition',
        'club': 'Simply Lift',
        'places': 1
    })
    assert b"Invalid competition or club." in response.data

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Non-existent Club',
        'places': 1
    })
    assert b"Invalid competition or club." in response.data
