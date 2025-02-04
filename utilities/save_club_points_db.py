import json

def save_club_points_db(clubs, file_path="clubs.json"):
    """ 
    Sauvegarde les points mis à jour dans le fichier JSON.
    """

    for club in clubs:
        club["points"] = str(club["points"]) # convertir int en str
    with open('clubs.json', 'w') as c:
        json.dump({"clubs": clubs}, c, indent=4)