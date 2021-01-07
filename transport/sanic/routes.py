
from configs.config import ApplicationConfig
from context import Context
from transport.sanic.endpoints.health import HealthEndpoint


def get_routes(config: ApplicationConfig, context: Context):
    return (
        HealthEndpoint(config, context, '/', methods=['GET', 'POST']),
    )
