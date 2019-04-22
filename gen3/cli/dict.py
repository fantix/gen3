import glob
import json
import os

import aiohttp
from ruamel.yaml import YAML

from . import with_loop, log
from ..dictionary import loader


@with_loop
async def main(args, loop):
    if args.url.startswith("http"):
        log.critical("Downloading dictionary JSON...")
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(args.url) as resp:
                data = await resp.json()

    elif os.path.isfile(args.url):
        log.critical("Reading dictionary JSON...")
        with open(args.url) as f:
            data = json.load(f)

    else:
        log.critical("Reading dictionary YAML source...")
        data = {}
        yaml = YAML(typ="safe")
        yaml.allow_duplicate_keys = True
        for path in glob.glob(f"{args.url}/*.yaml"):
            with open(path) as f:
                data[os.path.basename(path)] = yaml.load(f)

    loader.load(data)
