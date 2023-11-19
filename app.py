from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Fetch all movie data from Elasticsearch
def fetch_movie_data():
    # Initialize an empty list to store movie data
    movies_data = []

    # Elasticsearch query to fetch all movies
    es_query = {
        "query": {
            "match_all": {}  # Retrieve all documents
        },
        "size": 10000  # Adjust the size as needed to retrieve all documents
    }

    # Execute the Elasticsearch query on 'movies' index
    movie_result = es.search(index='movies', body=es_query)

    # Extract movie information if matches are found
    if movie_result['hits']['total']['value'] > 0:
        for hit in movie_result['hits']['hits']:
            movie_info = hit['_source']
            movies_data.append({
                'title': movie_info.get('title', ''),
                'description': movie_info.get('description', '')
                # Add more fields as needed
            })
    
    return movies_data

# Fetch movie data and calculate cosine similarity
movies_data = fetch_movie_data()

# Prepare movie descriptions for CountVectorizer
movie_descriptions = [movie['description'] for movie in movies_data]

# Create a CountVectorizer instance and fit_transform the movie descriptions
count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(movie_descriptions)

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Define the route for the homepage ('/')
@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

# Define an endpoint to get movie information based on the movie name
@app.route('/movie_info', methods=['GET'])
def get_movie_info():
    # Get the movie name from the request query parameters
    movie_name = request.args.get('movie_name')

    # Elasticsearch query to find the movie based on the given name
    es_query = {
        "query": {
            "match": {
                "title": {
                    "query": movie_name,
                    "fuzziness": "AUTO"  # Apply fuzzy matching
                }
            }
        }
    }

    # Execute the Elasticsearch query on 'movies' index
    movie_result = es.search(index='movies', body=es_query)

    # Extract movie information if a match is found
    movie_info = {}
    if movie_result['hits']['total']['value'] > 0:
        # Get the first hit (assumes unique titles, modify as needed)
        hit = movie_result['hits']['hits'][0]['_source']
        movie_info = {
            'title': hit['title'],
            'genre_ids': hit['genre_ids'],
            'original_language': hit['original_language'],
            'description': hit.get('description', ''),
            'popularity': hit['popularity'],
            'release_date': hit['release_date'],
            'vote_average': hit['vote_average'],
            'vote_count': hit['vote_count']
        }
        
        # Perform content-based filtering using cosine similarity
        indices = [i for i, movie in enumerate(movies_data)]
        idx = indices[movie_descriptions.index(movie_info['description'])]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]
        similar_movies = [movies_data[i] for i in movie_indices]
        movie_info['similar_movies'] = similar_movies
        
    else:
        return jsonify({'error': 'Movie not found'})

    # Return the movie information as JSON response
    return jsonify(movie_info)

if __name__ == '__main__':
    app.run(debug=True)