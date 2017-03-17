"""Simple redis based caching methods."""
import pickle
import time

import redis


def init(config_dict):
    """Define cache pool."""
    pool = redis.ConnectionPool(
        host='localhost', port=config_dict['redis_port'], db=0)
    return pool


def get_route(pool, route, timeout):
    """Get value for route as key."""
    conn = redis.Redis(connection_pool=pool)
    pickled_dict = conn.get(route)
    if pickled_dict is None:
        return -1
    else:
        resp = pickle.loads(pickled_dict)
        if (time.time() - resp["createdAt"] > timeout):
            return -1
        else:
            return resp["data"]


def set_route(pool, route, dict_response):
    """Set a key route to value."""
    conn = redis.Redis(connection_pool=pool)
    resp = {"data": dict_response, "createdAt": time.time()}
    pickle_dict = pickle.dumps(resp)
    conn.set(route, pickle_dict)


def reset(pool):
    """Reset whole dictionary."""
    conn = redis.Redis(connection_pool=pool)
    for i in conn.keys():
        conn.delete(i)
