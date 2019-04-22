import time

from tartiflette import Resolver


@Resolver("Query.now")
async def resolver_now(parent, args, context, info):
    print(parent, args, context, info)
    return str(time.time())
