import pytest
import json
import shutil
import os
from utilities.save_competitions_points_db import save_competitions_points_db

@pytest.fixture
def backup_competitions_json():
    """Crée une sauvegarde de `competitions.json` avant le test et la restaure après."""
    backup_file = "competitions_backup.json"
    original_file = "competitions.json"

    shutil.copy(original_file, backup_file)  # Sauvegarde
    yield original_file  # Fichier utilisé dans le test
    shutil.move(backup_file, original_file)  # Restauration après test

def test_save_competitions_db(backup_competitions_json):
    """Teste que `save_competitions_db()` modifie bien `competitions.json` et restaure l'original après test."""
    original_file = backup_competitions_json

    # Charger les compétitions avant modification
    with open(original_file, "r") as f:
        competitions_data = json.load(f)["competitions"]

    # Modifier une compétition
    competition_name = "Spring Festival"
    for competition in competitions_data:
        if competition["name"] == competition_name:
            competition["numberOfPlaces"] = "99"  # Changement test

    # Sauvegarder dans competitions.json (normalement utilisé par server.py)
    save_competitions_points_db(competitions_data)

    # Recharger pour vérifier la modification
    with open(original_file, "r") as f:
        updated_data = json.load(f)["competitions"]

    assert any(c["name"] == competition_name and c["numberOfPlaces"] == "99" for c in updated_data), \
        "Les places de la compétition n'ont pas été mises à jour."
