import os
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'


class PostgresConfig:
    name = os.getenv('POSTGRES_NAME', 'messager')
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', '123')
    host = os.getenv('POSTGRES_HOST', 'messager-db')
    port = os.getenv('POSTGRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
