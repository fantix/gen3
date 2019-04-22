from aiohttp import web

from . import with_loop
from .. import config
from .. import init


@with_loop
def main(args, loop):
    app = loop.run_until_complete(init.init_web())
    web.run_app(
        app, host=args.host or config.WEB_HOST, port=args.port or config.WEB_PORT
    )
