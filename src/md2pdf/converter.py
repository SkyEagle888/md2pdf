"""Markdown to PDF conversion engine."""

import io
import logging
import tempfile
from pathlib import Path
from typing import Optional

from markdown_pdf import MarkdownPdf, Section

from .assets import get_asset_base_dir

logger = logging.getLogger(__name__)


class Converter:
    """Handles Markdown to PDF conversion."""

    # Page size mapping for markdown-pdf
    PAGE_SIZES = {
        "A4": "A4",
        "A3": "A3",
        "A5": "A5",
        "Letter": "Letter",
        "Legal": "Legal",
        "Tabloid": "Tabloid",
    }

    def __init__(
        self,
        css: Optional[str] = None,
        page_size: str = "A4",
        margin: str = "10mm",
        base_dir: Optional[Path] = None,
    ):
        """
        Initialize the converter.

        Args:
            css: Optional path to custom CSS file (not used in markdown-pdf)
            page_size: Page size (A4, Letter, etc.)
            margin: Page margin (e.g., "10mm", "1in")
            base_dir: Base directory for resolving relative asset paths
        """
        self.base_dir = base_dir
        self.page_size = self.PAGE_SIZES.get(page_size, "A4")
        self.margin = margin
        self.custom_css = css  # Not used in markdown-pdf

    def convert(self, markdown_content: str) -> bytes:
        """
        Convert Markdown content to PDF.

        Args:
            markdown_content: The markdown text to convert

        Returns:
            PDF bytes

        Raises:
            Exception: If conversion fails
        """
        # Create a temporary file for the markdown content
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(markdown_content)
            tmp_path = tmp.name

        try:
            # Create section from the markdown file
            section = Section(
                "Document",
                toc=False,
                root=str(self.base_dir) if self.base_dir else ".",
                paper_size=self.page_size,
            )

            # Create PDF
            pdf = MarkdownPdf(
                toc_level=0,
                optimize=True,
            )
            pdf.add_section(section)

            # Save to bytes
            output = io.BytesIO()
            pdf.save(output)
            pdf_bytes = output.getvalue()

            return pdf_bytes

        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)

    def convert_file(self, input_path: Path, output_path: Path) -> None:
        """
        Convert a markdown file to PDF.

        Args:
            input_path: Path to input markdown file
            output_path: Path to output PDF file

        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: If conversion fails
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Set base directory for relative path resolution
        self.base_dir = get_asset_base_dir(input_path)

        # Create section from the markdown file
        section = Section(
            "Document",
            toc=False,
            root=str(self.base_dir) if self.base_dir else ".",
            paper_size=self.page_size,
        )

        # Create PDF
        pdf = MarkdownPdf(
            toc_level=0,
            optimize=True,
        )
        pdf.add_section(section)

        # Save to file
        pdf.save(str(output_path))

        logger.info(f"PDF created: {output_path}")
