import json
from flask import Flask,render_template,request,redirect,flash,url_for
from utilities.has_enough_places import has_enough_places
from utilities.cannot_book_more_places_than_availables import cannot_book_more_places_than_availables


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

    if not has_enough_places(placesRequired, club):
        flash("You cannot book more places than your points allow.")
        return render_template('welcome.html', club=club, competitions=competitions)


    if not cannot_book_more_places_than_availables(placesRequired,competition):
        flash('You can not book more places than availables')
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))