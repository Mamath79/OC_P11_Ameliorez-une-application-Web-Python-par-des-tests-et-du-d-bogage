import json
from flask import Flask,render_template,request,redirect,flash,url_for
from utilities.has_enough_places import has_enough_places
from utilities.cannot_book_more_places_than_availables import cannot_book_more_places_than_availables
from utilities.cannot_book_more_than_12_places import cannot_book_more_than_12_places
from utilities.cannot_book_places_in_past_competition import cannot_book_places_in_past_competition
from utilities.save_club_points_db import save_club_points_db
from utilities.save_competitions_points_db import save_competitions_points_db

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    matching_club = [club for club in clubs if club['email'] == request.form['email']]

    # verification d'existance de l'email et si non redirection
    if not matching_club:
        flash('sorry, email not found')
        return redirect('/')
    else:
        club = matching_club[0]
        return render_template('welcome.html',club=club,competitions=competitions)
    

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    placesRequired = int(request.form['places'])

    errors = []  # Liste pour stocker tous les messages d'erreur

    if not has_enough_places(placesRequired, club):
        errors.append("You can not book more places than your points allow.")

    if not cannot_book_more_places_than_availables(placesRequired, competition):
        errors.append("You can not book more places than availables")

    if not cannot_book_more_than_12_places(placesRequired):
        errors.append("You can not book more than 12 places.")

    if not cannot_book_places_in_past_competition(competition):
        errors.append("You cannot book places for a past competition.")

    # Si au moins une erreur a été détectée, on les affiche et on retourne
    if errors:
        for error in errors:
            flash(error)   
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Mise à jour des données
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired

    # Sauvegarde dans le fichier JSON
    save_club_points_db(clubs)

    # Sauvegarde des données des competitions dans les fichiers JSON
    save_competitions_points_db(competitions)

    flash("Great-booking complete!")
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display
@app.route('/points_display')
def points_display():
    """
    Affiche une page avec la liste des clubs et leurs points actuels.
    """
    return render_template('points_display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))