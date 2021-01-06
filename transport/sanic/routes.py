
from configs.config import ApplicationConfig
from transport.sanic.endpoints.health import HealthEndpoint


def get_routes(config: ApplicationConfig):
    return (
        HealthEndpoint(config, '/', methods=['GET', 'POST']),
    )
