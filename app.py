import logging
import os

from flask import Flask
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from api import api
from fetcher import Fetcher
from store import Store

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[logging.StreamHandler()])


def create_app(debug=False):
    app = Flask(__name__)
    api.init_app(app)

    app.sv_store = Store(os.environ.get('REDIS_URL'))

    if not debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        app.sv_fetcher = Fetcher(app.sv_store)
        REGISTRY.register(app.sv_fetcher)

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app(),
    })

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return app


if __name__ == "__main__":
    app = create_app(debug=True)
    app.run(host='0.0.0.0', debug=True)