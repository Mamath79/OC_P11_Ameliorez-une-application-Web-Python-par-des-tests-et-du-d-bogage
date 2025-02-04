import json

def save_competitions_points_db(competitions, file_path="competitions.json"):
    
    """
    Sauvegarde les modifications de competitions dans competitions.json
    """
    for competition in competitions:
        competition["numberOfPlaces"] = str(competition["numberOfPlaces"]) # convertir int en str
    with open('competitions.json', 'w') as f:
        json.dump({"competitions": competitions}, f, indent=4)


    