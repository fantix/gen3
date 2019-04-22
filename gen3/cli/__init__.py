import argparse
import asyncio
import logging

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--loop", choices=["asyncio", "uvloop"], default="uvloop")

subparsers = parser.add_subparsers(dest="command")

run = subparsers.add_parser("run")
run.add_argument("-H", "--host")
run.add_argument("-p", "--port", type=int)

db = subparsers.add_parser("db")
db.add_argument("upgrade")
db.add_argument("downgrade")

config_parser = subparsers.add_parser("config")
config_parser.add_argument("names", nargs="*")

dict_parser = subparsers.add_parser("dict")
dict_parser.add_argument("url")


def _install_loop(loop):
    log.critical("Creating %s event loop...", loop)
    if loop == "uvloop":
        try:
            # noinspection PyUnresolvedReferences
            import uvloop
        except ImportError:
            log.warning("Cannot import uvloop; fallback to asyncio.")
            loop = asyncio.new_event_loop()
        else:
            loop = uvloop.new_event_loop()
    else:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def with_loop(m):
    def wrapper(args):
        loop = _install_loop(args.loop)
        rv = m(args, loop)
        if asyncio.iscoroutine(rv):
            rv = loop.run_until_complete(rv)
        return rv

    return wrapper


def main():
    args = parser.parse_args()

    if args.command:
        mod = f"{__package__}.{args.command}"
        log.debug("Importing %s", mod)
        return __import__(mod, fromlist=__package__).main(args)

    else:
        parser.print_help()

        from .. import config

        print()
        print("config values")
        print()
        for key in config.__all__:
            print("  " + key)
        return 0
