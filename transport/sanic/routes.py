
from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context):
    return (
        endpoints.CreateUserEndpoint(
            config=config, context=context, uri='/user', methods=['POST'],
        ),
        endpoints.AuthUserEndpoint(
            config=config, context=context, uri='/auth', methods=['POST'],
        ),
        endpoints.MessagesEndpoint(
            config=config, context=context, uri='/msg', methods=['GET', 'POST'], auth_required=True
        ),
        endpoints.UserEndpoint(
            config=config, context=context, uri='/user/<uid:int>', methods=['GET'], auth_required=True,
        ),
        endpoints.EditUserEndpoint(
            config=config, context=context, uri='/user/edit', methods=['PATCH'], auth_required=True,
        ),
        endpoints.MessageEndpoint(
            config=config, context=context, uri='msg/<mid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True
        ),
    )
