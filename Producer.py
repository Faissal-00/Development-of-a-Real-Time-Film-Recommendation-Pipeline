from confluent_kafka import Producer
import requests
import json
import time

API_KEY = '962d46015e8beba5b5a2c444c7ab5ebe'
MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page={}"

# Define the Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Adjust the Kafka broker address as needed
    'client.id': 'randomuser_producer'
}

# Define the Kafka topic
kafka_topic = 'movies'

# Create a Kafka producer instance
producer = Producer(producer_config)

def fetch_and_publish_movies():
    page_number = 1  # Starting with the first page

    while True:
        response = requests.get(MOVIE_ENDPOINT.format(API_KEY, page_number))

        if response.status_code == 200:
            movies = response.json()['results']
            if not movies:  # If no more movies are returned, stop the loop
                break
            
            for movie in movies:
                # Extract specific columns: genre_ids, popularity, title
                data_to_send = {
                    'genre_ids': movie['genre_ids'],
                    'popularity': movie['popularity'],
                    'title': movie['title']
                }

                # Produce specific movie data to Kafka topic
                producer.produce(kafka_topic, key=str(movie['id']), value=json.dumps(data_to_send))
                print(f"Produced: {data_to_send['title']} to topic: {kafka_topic}")
            
            page_number += 1  # Move to the next page
            time.sleep(1)  # Add a small delay between requests (optional)
        else:
            print("Error fetching data from TMDb API")
            break  # Stop if there's an error in fetching data

    producer.flush()  # Ensure all messages are delivered

# Call the function to fetch and publish movies
fetch_and_publish_movies()