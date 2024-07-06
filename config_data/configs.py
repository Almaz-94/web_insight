from environs import Env
from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class S3Config(BaseConfig):
    access_key: str = 'None'
    secret_key: str = 'None'
    endpoint_url: str = 'None'
    bucket_name: str = 'None'


class NatsListenerConfig(BaseConfig):
    nats_server_url: str = 'nats://localhost:4222'
    nats_queue: str = 'web.wait.django'


class APIConfig(BaseConfig):
    api_host_url: str = ''
    get_all_assistant: str = ''
    get_one_assistant: str = ''
    start_youtube_process: str = ''
    start_s3_process: str = ''
    get_transcribed_text: str = ''
    get_summary_text: str = ''


class YoutubeApi(BaseConfig):
    youtube_api_key: str = ''


class PostgresDataBaseConfigs(BaseConfig):
    postgres_url: str = ''
    postgres_user: str = 'postgres'
    postgres_password: str = '1234'
    postgres_host: str = 'localhost'
    postgres_port: str = '5432'
    postgres_db: str = 'postgres'


class ProjectSettings(BaseConfig):
    language: str = 'ru'
    postgres: PostgresDataBaseConfigs = Field(default_factory=PostgresDataBaseConfigs)
    nats_listener: NatsListenerConfig = Field(default_factory=NatsListenerConfig)
    s3_config: S3Config = Field(default_factory=S3Config)
    api_config: APIConfig = Field(default_factory=APIConfig)
    youtube_api: YoutubeApi = Field(default_factory=YoutubeApi)


def load_config(path: str | None = None) -> ProjectSettings:
    env: Env = Env()
    env.read_env(path)
    return ProjectSettings(
        s3_config=S3Config(
            access_key=env('ACCESS_KEY'),
            secret_key=env('SECRET_KEY'),
            endpoint_url=env('ENDPOINT_URL'),
            bucket_name=env('BUCKET_NAME')
        ),
        nats_listener=NatsListenerConfig(
            nats_server_url=env("NATS_SERVER_URL"),
            nats_queue=env("NATS_QUEUE"),
        ),
        api_config=APIConfig(
            api_host_url=env("API_HOST_URL"),
            get_all_assistant=env('GET_ALL_ASSISTANT'),
            get_one_assistant=env('GET_ONE_ASSISTANT'),
            start_youtube_process=env('START_YOUTUBE_PROCESS'),
            start_s3_process=env('START_S3_PROCESS'),
            get_transcribed_text=env('GET_TRANSCRIBED_TEXT'),
            get_summary_text=env('GET_SUMMARY_TEXT'),
        ),
        pg_db_config=PostgresDataBaseConfigs(
            postgres_user=env('POSTGRES_USER'),
            postgres_password=env('POSTGRES_PASSWORD'),
            postgres_host=env('POSTGRES_HOST'),
            postgres_port=env('POSTGRES_PORT'),
            postgres_db=env('POSTGRES_DB'),
        ),
        youtube_api=YoutubeApi(
            youtube_api_key=env('YOUTUBE_API_KEY')
        ),
    )


settings = ProjectSettings()

if __name__ == '__main__':
    import os
    import django

    # Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Инициализируем Django
    django.setup()
    from main.models import Summary
    summary = Summary.objects.all()
    print(summary)
