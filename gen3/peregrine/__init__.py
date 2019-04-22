import logging
import os

from tartiflette import Engine
from tartiflette_aiohttp import register_graphql_handlers

from .. import config

log = logging.getLogger(__name__)


async def init(app):
    log.critical("Loading GraphQL SDL and install resolvers...")

    engine = app["engine"] = Engine(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "sdl"),
        modules=["gen3.peregrine.resolvers"],
    )
    register_graphql_handlers(
        app=app,
        engine=engine,
        subscription_ws_endpoint=f"{config.PEREGRINE_PREFIX}ws",
        executor_http_endpoint=f"{config.PEREGRINE_PREFIX}graphql",
        executor_http_methods=["POST"],
        graphiql_enabled=config.PEREGRINE_GRAPHIQL,
        graphiql_options=dict(endpoint=f"{config.PEREGRINE_PREFIX}graphiql"),
    )
    return engine
