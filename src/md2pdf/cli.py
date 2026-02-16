"""Command-line interface for md2pdf."""

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .converter import Converter


# Exit codes
EXIT_SUCCESS = 0
EXIT_GENERIC_FAILURE = 1
EXIT_INVALID_USAGE = 2
EXIT_INPUT_NOT_FOUND = 3
EXIT_CONVERSION_FAILURE = 4
EXIT_OUTPUT_NOT_WRITABLE = 5


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging based on verbosity level."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="md2pdf",
        description="Convert Markdown files to PDF with selectable text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  md2pdf input.md -o output.pdf
  md2pdf input.md --css custom.css --page-size Letter
  md2pdf README.md --margin 20mm --verbose
        """,
    )

    parser.add_argument(
        "input",
        type=str,
        help="Input markdown file path",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="PATH",
        help="Output PDF path (default: <input_basename>.pdf)",
    )

    parser.add_argument(
        "--page-size",
        type=str,
        default="A4",
        choices=["A4", "A3", "A5", "Letter", "Legal", "Tabloid"],
        help="Page size (default: A4)",
    )

    parser.add_argument(
        "--margin",
        type=str,
        default="10mm",
        help="Page margin (e.g., 10mm, 1in, 2cm)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print debug logs",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"md2pdf {__version__}",
    )

    return parser.parse_args(args)


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parsed = parse_args(args or sys.argv[1:])

    # Setup logging
    setup_logging(verbose=parsed.verbose, quiet=parsed.quiet)
    logger = logging.getLogger(__name__)

    # Validate input file
    input_path = Path(parsed.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {parsed.input}")
        return EXIT_INPUT_NOT_FOUND

    if not input_path.is_file():
        logger.error(f"Input path is not a file: {parsed.input}")
        return EXIT_INPUT_NOT_FOUND

    # Determine output path
    if parsed.output:
        output_path = Path(parsed.output)
    else:
        output_path = input_path.with_suffix(".pdf")

    # Validate output path is writable
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Try to create an empty file to check write permission
        output_path.touch()
        output_path.unlink()  # Remove the test file
    except Exception as e:
        logger.error(f"Output path not writable: {parsed.output or output_path} - {e}")
        return EXIT_OUTPUT_NOT_WRITABLE

    # Create converter
    try:
        converter = Converter(
            page_size=parsed.page_size,
            margin=parsed.margin,
        )
    except ValueError as e:
        logger.error(f"Invalid argument: {e}")
        return EXIT_INVALID_USAGE
    except Exception as e:
        logger.error(f"Failed to initialize converter: {e}")
        return EXIT_GENERIC_FAILURE

    # Perform conversion
    try:
        if not parsed.quiet:
            logger.info(f"Converting: {input_path} -> {output_path}")

        converter.convert_file(input_path, output_path, verbose=parsed.verbose)

        if not parsed.quiet:
            logger.info(f"Success! PDF created: {output_path}")

        return EXIT_SUCCESS

    except FileNotFoundError as e:
        error_msg = str(e)
        if "Missing image" in error_msg:
            logger.error(f"Missing asset: {error_msg}")
        else:
            logger.error(f"Input file not found: {error_msg}")
        return EXIT_INPUT_NOT_FOUND
    except PermissionError as e:
        logger.error(
            f"Permission denied: Cannot write to '{parsed.output or output_path}'. "
            f"Check that you have write access to the output directory."
        )
        return EXIT_OUTPUT_NOT_WRITABLE
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Conversion failed: {error_msg}")
        logger.error(
            "Tip: Run with --verbose to see detailed error information."
        )
        if parsed.verbose:
            import traceback

            traceback.print_exc()
        return EXIT_CONVERSION_FAILURE


if __name__ == "__main__":
    sys.exit(main())
