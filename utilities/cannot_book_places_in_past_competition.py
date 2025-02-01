from datetime import datetime
from flask import flash,render_template


def cannot_book_places_in_past_competition(competition):
    """
    Vérifier si la compétition est passée
    """
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        return False
    return True
        
