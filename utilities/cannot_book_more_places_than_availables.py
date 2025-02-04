def cannot_book_more_places_than_availables(placesRequired, competition):
    if placesRequired > int(competition["numberOfPlaces"]):
        return False
    return True
