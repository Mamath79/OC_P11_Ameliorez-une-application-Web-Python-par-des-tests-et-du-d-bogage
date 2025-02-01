import json

def save_competitions_points_db(competitions):
    
    """
    Sauvegarde les modifications de competitions dans competitions.json
    """

    with open('competitions.json', 'w') as f:
        json.dump({"competitions": competitions}, f, indent=4)