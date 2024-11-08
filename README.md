# Betting service

This project is a web application based on **FastAPI**. It is a small system that accepts user
bets on certain events (e.g. sports).

### Install and configure the project
### Use Docker Compose to build and run containers:
```
docker-compose up -d --build
```
This command builds Docker images and runs containers in the background.


### Perform database migrations
```
docker-compose exec -it api sh
alembic upgrade head
```


This command allows you to log into the container and perform database migrations.

## API Usage

### Port 8000
| Method | Route               | Description                                                            |
| ----- | ------------------ | ------------------------------------------------------------------- |
| GET   | /event             | Event creating.                    |
| POST  | /event/{event_id}      | Getting event by event_id |
| POST  | /events            | Getting all events that are still active. (deadline has not passed)                                      |
| GET   | /update_coefficient       | Changing the coefficient for an event.                     |
| GET   | /update_status | Changing the status for an event.       |
| GET   | /update_deadline         | Changing the deadline for an event.           |

### Port 8001
| Method | Route               | Description                                                            |
| ----- | ------------------ | ------------------------------------------------------------------- |
| POST  | /event             | Getting all events that are still active. (deadline has not passed)                    |
| POST  | /create_bet      | Bet creating. |
| POST  | /bets            | Getting all bets.                                      |

**Stack:**

- FastAPI
- PostgreSQL
- SQLAlchemy
- RabbitMQ
- Docker/Docker-compose
- Pytest
