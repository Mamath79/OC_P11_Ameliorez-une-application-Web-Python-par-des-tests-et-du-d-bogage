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


def test_access_show_summary_with_valid_email(client):
    """
    Teste que l'application gère correctement un e-mail valide en affichant la page de bienvenue.
    """
    club = loadClubs()

    response = client.post('/showSummary', data={'email': club[0]['email']})

    # Vérifie que l'utilisateur est redirigé vers la page de résumé (code 200)
    assert response.status_code == 200

    # Vérifie que le contenu attendu est présent dans la réponse (ex : e-mail ou points)
    assert bytes(club[0]['email'], 'utf-8') in response.data
    assert bytes(club[0]['points'], 'utf-8') in response.data
