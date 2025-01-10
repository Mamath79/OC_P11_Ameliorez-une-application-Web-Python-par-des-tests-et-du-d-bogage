import pytest
from server import app
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_past_competition(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',  # Date passée dans le fichier JSON
        'club': 'Simply Lift',
        'places': 5
    })
    assert b"You cannot book places for a past competition." in response.data
