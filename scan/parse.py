"""Parsing functions."""

from pathlib import Path
from PIL import Image
import imagehash

# Defaults
import os

# Internal modules
import helpers
import text


def identifier(path, key):
    """Parses an identifier based on it's suffix."""
    try:
        if key == "img":
            image = Image.open(path)
            return str(imagehash.average_hash(image))
    except:
        print("{} could not be hashed".format(path))

    return path.stem


def resolve_new_path(path, hash):
    """Checks if the path is correct. Corrects if it is not. Returns correct path."""

    new_path = Path(path.parent, "{}{}".format(hash, path.suffix))
    new_path = str(new_path)

    if str(path) != new_path:
      path.rename(new_path)

    return new_path


def resolve_tags(path, base, parent_root):
    """Resolves tags for PATH based on base list."""

    path = Path(path)
    parts = path.parts
    i = parts.index(parent_root)
    tags = [base, path.suffix] + list(parts[i +1 :-1])
    tags = list(map(helpers.uri_encode, tags))
    return tags


def resolve_thumbnail(path, hash, thumbnail_path, img):
    """Resolves thumbnail for PATH."""

    out_path = "{}/{}.jpg".format(thumbnail_path, hash)
    if not os.path.exists(out_path):
        size = 128, 128
        img.thumbnail(size)
        img.save(out_path, "JPEG")
    return "/static/thumb/{}.jpg".format(hash)


def doc(str_path, document, parent_root, thumbnail_path):
    """Indexes a documentument and assigns default tags."""

    path = Path(str_path)
    new_path = resolve_new_path(path, document["hash"]);

    document.update({
        "path": new_path,
        "tags": resolve_tags(new_path, document["html_tag"], parent_root),
    })

    try:
      img = Image.open(new_path)

      if "html_tag" in document and document["html_tag"] == "img":

        document.update({
            "identified_text": text.get_text(img),
            "thumbnail": resolve_thumbnail(new_path, document["hash"], thumbnail_path, img)
        })

    except Exception as e:
        print(e)


    return [document]
