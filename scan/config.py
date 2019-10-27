"""Helper for managing configurations."""

import json
import os
import pymongo


def load(path):
    """Initalize and loads the specificy config at path."""

    config = {}
    try:
        with open(path) as json_file:
            config = json.load(json_file)
    except OSError as error:
        print("could not load config file")
        raise error
    return config


def get_last_successful_scan(mongo):
    """Return when the last successful scan was performed."""

    doc = {"finished": {"$exists": True}}
    try:
        cursor = mongo.scan.find(doc).sort("finished", -1)
        result = cursor.next()
        finished = result["finished"]
    except pymongo.errors.CursorNotFound as error:
        print("no previous successful scan detected")
        finished = 0

    return finished

def set_last_successful_scan(mongo):
    """Sets current time to be the last successful scan."""

    with open('.tmp.json', 'w') as temp_file:
        temp_file.write("test")
    mongo.scan.insert_one({"finished": os.stat('.tmp.json').st_mtime})
