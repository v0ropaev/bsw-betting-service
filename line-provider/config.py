from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "rabbitmq"
    RABBITMQ_PASSWORD: str = "rabbitmq"
    RABBITMQ_QUEUE_NAME: str = "events"
    RABBITMQ_EXCHANGE_NAME: str = "events"

    @property
    def database_settings(self) -> dict:
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
        }

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    class Config:
        env_file = ".env"


settings = Settings()
