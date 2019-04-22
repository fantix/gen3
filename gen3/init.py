import logging

import edgedb
from aiohttp import web

from . import config

log = logging.getLogger(__name__)


async def init_db():
    log.critical("Creating EdgeDB connection pool...")

    return await edgedb.create_async_pool(
        database=config.EDGEDB_DATABASE,
        user=config.EDGEDB_USER,
        password=config.EDGEDB_PASSWORD,
    )


async def init_web(peregrine=True):
    app = web.Application()

    app["db"] = await init_db()

    if peregrine:
        from . import peregrine

        await peregrine.init(app)

    return app
