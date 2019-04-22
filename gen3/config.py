EDGEDB_DATABASE = "gen3"
EDGEDB_USER = "gen3"
EDGEDB_PASSWORD = "gen3"

WEB_HOST = "0.0.0.0"
WEB_PORT = 8080

PEREGRINE_PREFIX = "/"
PEREGRINE_GRAPHIQL = True


__all__ = list(
    sorted(key for key in globals().keys() if key.isupper() and not key.startswith("_"))
)


def _load():
    import json
    import os

    for key in __all__:
        value = globals()[key]
        val_type = type(value)
        value = os.environ.get("GEN3_" + key, None)
        if value is not None:
            if val_type is int:
                value = int(value)
            elif val_type is bool:
                value = value in {"true", "True", "yes", "1"}
            elif val_type not in {type(None), str}:
                value = json.loads(value)
            globals()[key] = value


_load()
del _load
