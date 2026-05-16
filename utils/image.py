# ─────────────────────────────────────────────
# utils/image.py
# Helpers for loading and encoding local images
# ─────────────────────────────────────────────

import base64
from pathlib import Path


def get_image_b64(filename: str, assets_dir: str = "assets") -> str:
    """
    Load a local image from the assets directory and return a
    base64 data URI string suitable for embedding in HTML/CSS.

    Args:
        filename:   Image filename, e.g. "Pantnagar_logo.jpg"
        assets_dir: Folder relative to project root (default: "assets")

    Returns:
        A data URI string like "data:image/jpg;base64,..."
    """
    # Resolve path relative to the project root (two levels up from this file)
    base = Path(__file__).resolve().parent.parent
    path = base / assets_dir / filename

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    ext = path.suffix.lstrip(".")   # e.g. "jpg"
    return f"data:image/{ext};base64,{data}"