from sanic import Sanic

from configs.config import ApplicationConfig
from context import Context
from hooks import  init_db_sqlite
from transport.sanic.routes import get_routes


def configure_app(config: ApplicationConfig, context: Context):

    init_db_sqlite(context)

    app = Sanic(__name__)

    for handler in get_routes(config, context):
        app.add_route(
            handler=handler,
            methods=handler.methods,
            uri=handler.uri,
        )

    return app
