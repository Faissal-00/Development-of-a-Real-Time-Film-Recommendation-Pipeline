# Project Context

In this project, I developed a real-time system that manages the entire pipeline from data collection to user recommendations. The main tasks included:

## Kafka Configuration
I set up a Kafka cluster and configured producers to stream user interaction data to specific topics.

## Processing with Spark Streaming
I created pipelines to consume data from Kafka, applied various transformations, and sent the data to Elasticsearch. For instance:
- Enriched the data by combining titles and summaries into a "description" field.
- Normalized fields like average ratings and popularity.
- Converted date strings into date types.
- Included additional transformations, such as flattening IDs, to facilitate visualization.

## Modeling and Storage in Elasticsearch
I designed indices and data models in Elasticsearch to effectively store movie and user information.

## Recommendation API Development
I programmed a RESTful API using Flask that interacts with Elasticsearch to retrieve and serve recommendations.

## Visualization with Kibana
I created dashboards in Kibana to visualize data and support decision-making. Example visualizations include:
- Movie release distribution
- Top 10 popular films
- Average ratings by genre
- Linguistic distribution of films
- Top 10 films with the most votes
- Movie rating distribution

This project involved building a comprehensive real-time data processing and recommendation system, utilizing advanced technologies to provide valuable and actionable insights for users.
