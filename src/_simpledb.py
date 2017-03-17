"""Methods for storing stats."""
import pymongo
from pymongo import MongoClient


def update(key, value, metadata):
    """Update stats."""
    try:
        connection = MongoClient("localhost", 27017)
    except pymongo.errors.ConnectionFailure, e:
        return [-1, "Could not connnect do MongoDB %s" % e]

    db = connection.storage
    url_mapping = db.url_mapping
    '''analytics = db.analytics'''

    url_mapping.update({'key': key}, {"$set": {"value": value}}, upsert=True)

    '''endpoint_exists = queries.find({"key": key})
    try:
        val = endpoint_exists.next()["value"]
        queries.update({'endpoint': route}, {
                       "$set": {"value": val + 1}}, upsert=True)
    except StopIteration, e:
        queries.update({'endpoint': route}, {
                       "$set": {"value": 1}}, upsert=True)
    '''


def show(key):
    """Show stats."""
    try:
        connection = MongoClient("localhost", 27017)
    except pymongo.errors.ConnectionFailure, e:
        return [-1, "Could not connnect do MongoDB %s" % e]

    db = connection.storage
    url_mapping = db.url_mapping
    '''analytics = db.analytics'''

    endpoint_exists = url_mapping.find({"key": key})
    try:
        return [0, endpoint_exists.next()["value"]]
    except:
        return [-1, "Short url %s does not exists" % key]
