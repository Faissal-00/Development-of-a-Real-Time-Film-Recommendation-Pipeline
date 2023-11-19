# Connect to the API and get the data moviedb.org
import requests
import json

API_KEY ='bd31e9c27bfa14a6403e1b56a1b2aa13'
MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&sort_by=created_at.asc&page={}"
# MOVIE_ENDPOINT = "https://api.themoviedb.org/3/person/changes?api_key={}&page=1"
# MOVIE_ENDPOINT = "https://api.themoviedb.org/3/person/2125889?api_key={}"
# MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/507089?api_key={}&language=en-US"
# MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/507089/reviews?api_key={}&language=en-US"
# MOVIE_ENDPOINT = "https://api.themoviedb.org/3/review/653a4ad08a0e9b010b29016c?api_key={}&language=en-US"

# Get the data from the API
def get_data():
    response = requests.get(MOVIE_ENDPOINT.format(API_KEY, 5))
    return response.json()

data = get_data()
js = json.dumps(data, indent=4, sort_keys=True)
print(js)