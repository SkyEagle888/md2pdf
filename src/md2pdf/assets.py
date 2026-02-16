"""Asset handling for md2pdf."""

import os
from pathlib import Path
from urllib.parse import unquote


def resolve_image_path(image_src: str, base_dir: Path) -> Path:
    """
    Resolve a relative image path to an absolute path.

    Args:
        image_src: The image source from markdown (e.g., "./images/logo.png")
        base_dir: The directory containing the markdown file

    Returns:
        Absolute Path to the image file

    Raises:
        FileNotFoundError: If the image file doesn't exist
    """
    # Decode URL-encoded characters (e.g., %20 -> space)
    decoded_src = unquote(image_src)

    # Handle both relative paths and URLs
    if decoded_src.startswith(("http://", "https://", "data:")):
        # External URLs or data URIs - return as-is (WeasyPrint handles them)
        return Path(decoded_src)

    # Resolve relative path against base directory
    image_path = (base_dir / decoded_src).resolve()

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if not image_path.is_file():
        raise FileNotFoundError(f"Image path is not a file: {image_path}")

    return image_path


def get_asset_base_dir(markdown_file: Path) -> Path:
    """
    Get the base directory for resolving relative asset paths.

    Args:
        markdown_file: Path to the markdown file

    Returns:
        The directory containing the markdown file
    """
    return markdown_file.resolve().parent
