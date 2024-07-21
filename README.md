Project Context
In this project, I developed a real-time system that handles the entire pipeline from collecting data to delivering user recommendations. The main tasks included:

Kafka Configuration: I set up a Kafka cluster and configured producers to stream user interaction data to specific topics.
Processing with Spark Streaming: I created pipelines to consume data from Kafka, applied various transformations, and sent the data to Elasticsearch. For instance, I enriched the data by combining titles and summaries into a "description" field, normalized fields like average ratings and popularity, and converted date strings into date types. I also included additional transformations, such as flattening IDs, to facilitate visualization.
Modeling and Storage in Elasticsearch: I designed indices and data models in Elasticsearch to effectively store movie and user information.
Recommendation API Development: I programmed a RESTful API using Flask that interacts with Elasticsearch to retrieve and serve recommendations.
Visualization with Kibana: I created dashboards in Kibana to visualize data and support decision-making. Examples of visualizations include movie release distribution, top 10 popular films, average ratings by genre, linguistic distribution of films, top 10 films with the most votes, and movie rating distribution.
This project involved building a comprehensive real-time data processing and recommendation system, utilizing advanced technologies to provide valuable and actionable insights for users.
