from flask import render_template,flash


def has_enough_places(placesRequired:int,club,competitions):
    # Vérification qu'un club ne peut reserver plus de places que de places disponibles
    if placesRequired > int(club['points']):
        flash("You cannot book more places than your points allow.")
        return render_template('welcome.html', club=club, competitions=competitions)