import logging
import os
from collections import namedtuple
from copy import deepcopy

from jsonschema import RefResolver, validate
from ruamel.yaml import YAML

log = logging.getLogger(__name__)
ResolverPair = namedtuple("ResolverPair", ["resolver", "source"])
METASCHEMA_PATH = "metaschema.yaml"
DEFINITIONS_PATHS = ["_definitions.yaml", "_terms.yaml"]
SETTINGS_PATH = "_settings.yaml"


def load(schemas):
    log.critical("Parsing dictionary...")
    resolvers = {
        key: ResolverPair(RefResolver("{}#".format(key), schema), schema)
        for key, schema in schemas.items()
    }
    schemas = {
        schema["id"]: _resolve_schema(schema, deepcopy(schema), resolvers)
        for path, schema in schemas.items()
        if path not in [METASCHEMA_PATH] + DEFINITIONS_PATHS + [SETTINGS_PATH]
    }

    log.critical("Validating dictionary format...")
    yaml = YAML(typ="safe")
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "schema", METASCHEMA_PATH
    )
    with open(path) as f:
        meta = yaml.load(f)
    for s in schemas.values():
        log.info("Validating '%(title)s'", s)
        validate(s, meta)

        def assert_link_is_also_prop(link_):
            assert (
                link_ in s["properties"]
            ), "Entity '{}' has '{}' as a link but not property".format(s["id"], link_)

        for link in [l["name"] for l in s["links"] if "name" in l]:
            assert_link_is_also_prop(link)
        for subgroup in [l["subgroup"] for l in s["links"] if "name" not in l]:
            for link in [l["name"] for l in subgroup if "name" in l]:
                assert_link_is_also_prop(link)
    return schemas


def _resolve_reference(value, root, resolvers):
    base, ref = value.split("#", 1)

    if base:
        resolver, new_root = resolvers[base]
        referrer, resolution = resolver.resolve(value)
        _resolve_schema(resolution, new_root, resolvers)
    else:
        resolver = RefResolver("#", root)
        referrer, resolution = resolver.resolve(value)

    return resolution


def _resolve_schema(obj, root, resolvers):
    ref_key = "$ref"
    if isinstance(obj, dict):
        all_ref_keys = [k for k in obj.keys() if k.startswith(ref_key)]
        for key in all_ref_keys:
            val = obj.pop(key)
            obj.update(_resolve_reference(val, root, resolvers))
        return {k: _resolve_schema(v, root, resolvers) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_resolve_schema(item, root, resolvers) for item in obj]
    else:
        return obj
