from flask import flash,redirect,render_template


def matching_club_loging(matching_club,competitions):
    if not matching_club:
        flash('sorry, email not found')
        return redirect('/')
    else:
        club = matching_club[0]
        return render_template('welcome.html',club=club,competitions=competitions)