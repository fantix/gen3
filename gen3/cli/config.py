from .. import config


def main(args):
    for key in config.__all__:
        if not getattr(args, "names", None) or key in args.names:
            print(f"{key}={getattr(config, key)}")
