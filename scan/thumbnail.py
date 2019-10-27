"""Create thumbnails for resources."""

import os

def create_thumbnail(image, out_path):
    """Creates a new thumbnail for supported file IMAGE types at OUT_PATH."""

    if out_path.suffix != ".gif" and not os.path.exists(out_path):
        image.save(out_path, optimize=True, quality=30)
