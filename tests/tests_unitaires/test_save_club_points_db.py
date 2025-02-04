import pytest
import json
import shutil
import os
from utilities.save_club_points_db import save_club_points_db


@pytest.fixture
def backup_clubs_json():
    """Crée une sauvegarde de `clubs.json` avant le test et la restaure après."""
    backup_file = "clubs_backup.json"
    original_file = "clubs.json"

    shutil.copy(original_file, backup_file)  # Sauvegarde
    yield original_file  # Fichier utilisé dans le test
    shutil.move(backup_file, original_file)  # Restauration après test


def test_save_club_points_db(backup_clubs_json):
    """Teste que `save_club_points_db()` modifie bien `clubs.json` et restaure l'original après test."""
    original_file = backup_clubs_json

    # Charger les clubs avant modification
    with open(original_file, "r") as f:
        clubs_data = json.load(f)["clubs"]

    # Modifier un club
    club_name = "Simply Lift"
    for club in clubs_data:
        if club["name"] == club_name:
            club["points"] = "999"  # Changement test

    # Sauvegarder dans clubs.json (normalement utilisé par server.py)
    save_club_points_db(clubs_data)

    # Recharger pour vérifier la modification
    with open(original_file, "r") as f:
        updated_data = json.load(f)["clubs"]

    assert any(
        c["name"] == club_name and c["points"] == "999" for c in updated_data
    ), "Les points du club n'ont pas été mis à jour."
