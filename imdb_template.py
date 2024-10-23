import requests
from config import IMDB_API_KEY

def get_movie_info(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={IMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return {
                "title": data['Title'],
                "year": data['Year'],
                "rating": data['imdbRating'],
                "genre": data['Genre'],
                "plot": data['Plot'],
                "poster": data['Poster'],
                "link": f"https://www.imdb.com/title/{data['imdbID']}/"
            }
    return None
