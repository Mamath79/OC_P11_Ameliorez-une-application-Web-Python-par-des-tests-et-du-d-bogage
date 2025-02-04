from flask import render_template, flash


def has_enough_places(placesRequired: int, club):
    # Vérification qu'un club ne peut reserver plus de places que de places disponibles
    if placesRequired > int(club["points"]):
        return False
    return True
