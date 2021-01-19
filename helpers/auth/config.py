import os
from dotenv import load_dotenv

load_dotenv()


class jwtConfig:
    secret = os.getenv('host', 'Super secret secret')
