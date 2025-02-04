from server import app, loadClubs
import pytest


@pytest.fixture
def client():
    """
    Configure un client de test Flask pour simuler des requêtes HTTP.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_point_display(client):
    """
    Verifie que la page des points affiche bien les clubs et leurs points respectifs
    """

    # Charger le fichier clubs.json
    clubs = loadClubs()

    # Acceder à la page points_display.html
    response = client.get("/points_display")

    assert response.status_code == 200

    # Verifie que chaque club et ses points sont bien afficher dans la page
    for club in clubs:
        assert bytes(club["name"], "utf-8") in response.data
        assert bytes(club["points"], "utf-8") in response.data
