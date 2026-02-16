"""Asset handling for md2pdf."""

from pathlib import Path


def get_asset_base_dir(markdown_file: Path) -> Path:
    """
    Get the base directory for resolving relative asset paths.

    Args:
        markdown_file: Path to the markdown file

    Returns:
        The directory containing the markdown file
    """
    return markdown_file.resolve().parent
