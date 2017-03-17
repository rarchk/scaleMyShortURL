"""URL shortner API server."""
import argparse
import logging
import re
import time
import gzip
import StringIO
import hashlib

import _cache

import _epollserver as epoll

import requests

import _simpledb

import _utilities

__author__ = 'Ronak Kogta<rixor786@gmail.com>'
__description__ = '''URL shortner API '''
_default_response_ = '''URL shortner API server.\r\n
Have got no response for above query
Please refer https://github.com/rarchk/scaleMyShortURL#examples'''

logger = logging.getLogger()

# API endpoints with their query points
API_ENDPOINTS = {
    "create": ["url=", "&alias="],
    "get": ["short_url="],
    "analytics": ["short_url="]
}


def parse_config(cmdline_opts):
    """Parse configuration from commmand line."""
    cmdline_opts.add_argument(
        '-p', '--port', help='Enter port number', default=8001)
    cmdline_opts.add_argument(
        '--host', help='Enter host name', default='localhost')
    cmdline_opts.add_argument(
        '-c', '--config', help='Enter config file', default='config.json')


def request_handler(epoll_context, parameters):
    """Application level request handler."""
    request, _, _ = epoll_context
    config_dict, redis_pool = parameters

    try:
        route = get_route(request, config_dict)

        return ['200', "fs\r\n", str(route)]

    except Exception as e:
        logger.error("Error in handling request:%s" % (e))
        return ['400', "fsd\r\n", _default_response_]


def get_route(request, config_dict):
    """Get routes for api endpoints."""
    try:
        route = re.search("GET (.*) HTTP", request).group(1)
    except:
        logger.error("Not a get request from client %s" % request)
        raise Exception
        return
    routers = route.split("/")

    if routers[3] == "create":
        try:
            _, url, alias = route.split("=")
            if (alias == 1):
                return config_dict['service'] + alias
            else:
                return config_dict['service'] + get_short_url_hash(url, config_dict)
        except:
            _, url = route.split("=")
            return config_dict['service'] + get_short_url_hash(url, config_dict)
    elif routers[3] == "get":
        _, short_url = route.split("=")
        short_url_hash = short_url.split(config_dict['service'])[1]
        status, url = _simpledb.show(short_url_hash)
        if (status == -1):
            logger.error(url)
            return
        return requests.get(url)

    elif routers[3] == "analytics":
        pass


def get_short_url_hash(url, config_dict):
    """Generate short url."""
    h = hashlib.new(config_dict['hash'])
    h.update(url)
    return h.hexdigest()[:config_dict['short_url_length']]


if __name__ == '__main__':
    cmdline_opts = argparse.ArgumentParser(description=__description__)
    parse_config(cmdline_opts)
    args = cmdline_opts.parse_args()

    config_dict = _utilities.load_config(args.config)
    _utilities.init_logger(logger, config_dict)
    redis_pool = _cache.init(config_dict)

    this_server = epoll.Server(int(args.port), args.host, request_handler, [
                               config_dict, redis_pool])
    this_server.run()
