import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
    club = [club for club in clubs if club['email'] == request.form['email']][0]
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

    # Vérification des entrées
    if not competition or not club:
        flash("Invalid competition or club.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired <= 0:
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification des conditions spécifiques
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > int(club['points']):
        flash("You cannot book more places than your points allow.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Mise à jour des données en cas de succès
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash(f"Great! Booking complete. You have {club['points']} points remaining.")
    return render_template('welcome.html', club=club, competitions=competitions)




# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))