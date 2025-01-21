# STEPS TO RUN

<details>
  <summary><h2>Python</h2></summary>

  1. We will need to use python 3.10 or above to run this.
  2. This constraint will cause issues when running poetry since this is a hard requirement.
  3. You can use asdf version manager to easily install different python interpreter. Simply go to the project root and enter 
      ```bash
     asdf install
      ```
  4. Once your python interpreter is ready, please install poetry.
      ```bash
      pip install poetry
      ```
      
  5. Once Poetry is installed, we use poetry to create a new virtual env and install all dependencies.
     ```bash
     poetry install
     ``` 
</details>

<details>
  <summary><h2>Redis</h2></summary>
  
  1. We will be using Redis as our message queue and cache store.
  2. We will simply use docker to run redis.
  3. Use `https://www.docker.com/` to download docker.
  4. Once docker deamon is up and running. We will start a container with redis in it and expose the port for our application to use.
     ```bash
     docker run -d -p6379:6379 redis
     ```
     This will pull the latest redis image and run it in detatched mode. Note you 
</details>

<details>
  <summary><h2>FastAPI Application</h2></summary>
  
  We are now ready to start our application.
  ```bash
  poetry run uvicorn main:app --port 8000 --reload
  ```
  This will start our application on port 8000. 
  You may visit `http://localhost:8000/docs` to check swagger docs.
</details>

<details>
  <summary><h2>Celery</h2></summary>
  
  In a new terminal we now start our Celery application
  ```bash
  poetry run celery -A app.task_queue.celery_app worker --loglevel=INFO --concurrency=1
  ```
</details>

# Design Decisions

  1. The EP is designed to simply queue the scraping of the page requested. This is done because the scraping could mean a lot of retries and and network calls which will be better suited for background processing.
  2. This is where celery comes into picture. Celery tasks are designed to scrape one page at a time. Celery workers are set up to only perform one task at a time but configuration for the same has been given and can be changed.
  3. The code is written to not need a env file however if one chooses to provide an env file it will override the base settings in config. Simply export the env file variables. This is set up so as to when we have an ECS running we can have env variables set via task definition or AWS Secrets.
  4. Endpoint router uses a dependency injector for authenticating incoming requests with a static token.
  5. We are using abstract classes where ever possible so as to extend the same and move on to a new provider with ease. For example the cache store can be extended to use a new adapter instead of Redis. This means we simply implement the functions and change the initiation of cache store to move to a new cache provider.
  6. The Databse is structured to mimic a real database as much as possible. This means a json file is opened and its TextWrapper is being passed as connection.
  7. A similar set up is being used for Notification. To start sending notifications to a new place, say slack or websocket, we will simply need to extend the base notifier and implement the functions.
  8. Once the new class is ready we simply add it to notificatino sender. NotificationSender takes care of sending all notifications. Other services need to only send the payload of Notification to NotificationSender.

# Improvemets
  1. Rate limiter can be implemented for scraping network calls. Since we are already using Redis, We can have a luna script that adds the time stamp of last request made. This way we can space out the requests to the scraping website so as to not get blocked.
  2. This also ensures that if workers are on different machines we will space out the requests.
  3. Instead of updating the entry, we are simply appending the list of products. This logic can be improved upon to search through json and and then update. 
