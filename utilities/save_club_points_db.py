import json

def save_club_points_db(clubs):
    """ 
    Sauvegarde les points mis à jour dans le fichier JSON.
    """
    with open('clubs.json', 'w') as c:
        json.dump({"clubs": clubs}, c, indent=4)