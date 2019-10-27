"""Scans directories and indexes them in a database."""
# pylint: disable=no-member
# pylint: disable=global-statement

# Imports
import time
import atexit
import os.path
import itertools

# Imported modules
import pymongo
import progressbar

# Internal modules
import config
import helpers
import parse

CONFIG = config.load("config.json")
TO_BULK_INSERT = []

CLIENT = pymongo.MongoClient("mongodb://{host}:{port}/".format_map(CONFIG["mongodb"]))
DB = CLIENT[CONFIG["mongodb"]["database"]]

if not DB.model.count_documents({}):
    no_check = True

CONFIG["finished"] = config.get_last_successful_scan(DB)
if float(os.stat("config.json").st_mtime) > CONFIG["finished"]:
    CONFIG["finished"] = 0


def bulk_insert():
    """Performs a bulk insert operation."""

    if not TO_BULK_INSERT:
        return
    DB.model.insert_many(TO_BULK_INSERT)

atexit.register(bulk_insert)


def __init__():
    global TO_BULK_INSERT

    paths = helpers.list_paths(CONFIG)

    if not paths:
      return

    bar = progressbar.ProgressBar(max_value=len(paths), redirect_stdout=True)

    for num, doc in enumerate(paths):
        bar.update(num)

        path = doc["path"]
        print(path)

        doc["hash"] = parse.identifier(doc["path"], doc["html_tag"])

        find_existing_cursor = DB.model.find(
            {"hash": doc["hash"]},
            {"_id": 0, "path": 1}
        )

        try:
            find_existing = find_existing_cursor.next()
            path = str(path)
            if find_existing["path"] != path:
                if os.path.exists(find_existing["path"]):
                    print("duplicate file {}".format(path))
                    # os.remove(path)
                else:
                    DB.model.update_one({"hash": doc["hash"]}, {"$set":{"path": path}})
                    print("{} moved to {}".format(find_existing["path"], path))
        except:
            TO_BULK_INSERT += parse.doc(path, doc, CONFIG["tag"]["parent"], CONFIG["thumbnails"])


__init__()
config.set_last_successful_scan(DB)
