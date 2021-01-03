from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json

app = Sanic(__name__)


@app.route('/', methods=['GET', 'POST', ])
async def health_endpoint(request: Request) -> HTTPResponse:

    response = {
        'hello': 'world'
    }

    if 'POST' in request.method:
        response.update(request.json)

    return json(body=response, status=200)


app.run(
    host='localhost',
    port=8000,
)
