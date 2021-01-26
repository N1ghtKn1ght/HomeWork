from helpers.auth.config import jwtConfig
from transport.sanic.config import SanicConfig
from db.config import SQLiteConfig, PostgresConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: PostgresConfig
    jwt: jwtConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = SQLiteConfig()
        self.jwt = jwtConfig()
        #self.database = PostgresConfig()
