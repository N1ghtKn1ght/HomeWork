
from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context):
    return (
        endpoints.UserEndpoint(config=config, context=context, uri='/user', methods=['GET', 'POST'])
    )
