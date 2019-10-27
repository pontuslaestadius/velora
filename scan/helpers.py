"""General purpose helper functions."""

import re
import os
from pathlib import Path


def uri_encode(string):
    """Escapes a string usable for uri encoding."""
    return re.sub(r"[^a-z0-9]", "", string.lower())


def list_paths(config):
    """Retrieves all files we care about."""

    directories = config["directories"]
    finished = config["finished"]
    max_size = config["max_size"]
    allowed_suffixes = config["suffixes"]["video"] + config["suffixes"]["img"]

    files = []

    for directory in directories:
        for r, d, f in os.walk(directory):
            for file in f:
                path = Path(os.path.join(r, file))
                stat = os.stat(path)

                # Checks if the file has been modified, or created at a later date than
                # our last successful scan. And is of an allowed file type.
                if stat.st_size < max_size and (stat.st_mtime > finished or stat.st_ctime > finished) and path.suffix.lower() in allowed_suffixes and os.path.isfile(path):
                    for key in config["suffixes"]:
                        if path.suffix.lower() in CONFIG["suffixes"][key]:
                            files.append({"path": path, "html_tag": key})
                            break

    return files
