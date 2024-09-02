from pydantic.v1 import BaseSettings
import os

class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class loads configuration values from environment variables or an `.env` file.

    Attributes:
        database_hostname (str): Hostname of the database server.
        database_port (str): Port of the database server.
        database_password (str): Password for the database.
        database_name (str): Name of the database.
        database_username (str): Username for the database.
        secret_key (str): Secret key used for security purposes (e.g., for encoding tokens).
        algorithm (str): Algorithm used for encoding tokens (e.g., "HS256").
        access_token_expire_minutes (int): Expiry time for access tokens in minutes.
        refresh_token_expire_days (int): Expiry time for refresh tokens in days.

    Configuration:
        The `.env` file is located in the parent directory of the current file.
        This is specified by the `env_file` attribute in the `Config` subclass.

    Usage:
        To use these settings, instantiate the `Settings` class:
        ```python
        settings = Settings()
        ```
        Access the configuration values using the attributes:
        ```python
        print(settings.database_hostname)
        ```

    Example `.env` file:
        DATABASE_HOSTNAME=localhost
        DATABASE_PORT=5432
        DATABASE_PASSWORD=secretpassword
        DATABASE_NAME=mydatabase
        DATABASE_USERNAME=myusername
        SECRET_KEY=supersecretkey
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30
        REFRESH_TOKEN_EXPIRE_DAYS=7
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config:
        env_file = env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"


settings = Settings()