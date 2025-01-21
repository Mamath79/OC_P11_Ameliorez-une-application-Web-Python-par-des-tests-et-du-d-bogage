from server import app, loadClubs
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client :
        yield client

def test_point_display():
    """
    Verifie que  page des points affiche bien les clubs et leurs points respectifs
   """
    
    # Charger le fichier clubs.json
    clubs = loadClubs()

    # Acceder à la page points_display.html
    response = client.get('/points_display')

    assert response.status ==200 

    # Verifie que chaque club et ses points sont bien afficher dans la page 
    for club in clubs:
        assert club['name'].encode() in response.data
        assert str(club['points']).encode() in response.data