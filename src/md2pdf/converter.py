"""Markdown to PDF conversion engine."""

import re
from pathlib import Path
from typing import Optional

import pygments
from markdown_pdf import MarkdownPdf, Section
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer

# Explicit lexer imports for common documentation languages
# Only these lexers will be included in the PyInstaller build
from pygments.lexers.python import PythonLexer
from pygments.lexers.javascript import JavascriptLexer, TypeScriptLexer
from pygments.lexers.shell import BashLexer, PowerShellLexer
from pygments.lexers.data import JsonLexer, YamlLexer
from pygments.lexers.html import HtmlLexer, XmlLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.sql import SqlLexer
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.go import GoLexer
from pygments.lexers.rust import RustLexer
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.diff import DiffLexer
from pygments.lexers.configs import IniLexer, TOMLLexer

from .assets import get_asset_base_dir

# Map language aliases to lexer classes (explicit, no dynamic loading)
LEXER_MAP: dict[str, type[TextLexer]] = {
    # Python
    "python": PythonLexer,
    "py": PythonLexer,
    # JavaScript
    "javascript": JavascriptLexer,
    "js": JavascriptLexer,
    # TypeScript
    "typescript": TypeScriptLexer,
    "ts": TypeScriptLexer,
    # Bash/Shell
    "bash": BashLexer,
    "sh": BashLexer,
    "shell": BashLexer,
    "zsh": BashLexer,
    # PowerShell
    "powershell": PowerShellLexer,
    "ps1": PowerShellLexer,
    "pwsh": PowerShellLexer,
    # Data formats
    "json": JsonLexer,
    "yaml": YamlLexer,
    "yml": YamlLexer,
    # Web
    "html": HtmlLexer,
    "xml": XmlLexer,
    "css": CssLexer,
    # Database
    "sql": SqlLexer,
    # JVM languages
    "java": JavaLexer,
    "kotlin": JavaLexer,  # Fallback to Java lexer
    "scala": JavaLexer,  # Fallback to Java lexer
    # System languages
    "go": GoLexer,
    "rust": RustLexer,
    "c": CLexer,
    "cpp": CppLexer,
    "c++": CppLexer,
    # Markup
    "markdown": MarkdownLexer,
    "md": MarkdownLexer,
    # Config files
    "ini": IniLexer,
    "toml": TOMLLexer,
    # Other
    "diff": DiffLexer,
}

# Valid margin format: number followed by unit (mm, cm, in, pt, px)
MARGIN_PATTERN = re.compile(r"^\d+(\.\d+)?(mm|cm|in|pt|px)$")


def validate_margin(margin: str) -> None:
    """
    Validate margin format.

    Args:
        margin: Margin string (e.g., "10mm", "1in", "2.5cm")

    Raises:
        ValueError: If margin format is invalid
    """
    if not MARGIN_PATTERN.match(margin):
        raise ValueError(
            f"Invalid margin format: '{margin}'. "
            f"Expected format: <number><unit> (e.g., '10mm', '1in', '2.5cm'). "
            f"Valid units: mm, cm, in, pt, px"
        )


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
        page_size: str = "A4",
        margin: str = "10mm",
        base_dir: Optional[Path] = None,
    ):
        """
        Initialize the converter.

        Args:
            page_size: Page size (A4, Letter, etc.)
            margin: Page margin (e.g., "10mm", "1in")
            base_dir: Base directory for resolving relative asset paths
        """
        validate_margin(margin)
        self.base_dir = base_dir
        self.page_size = self.PAGE_SIZES.get(page_size, "A4")
        self.margin = margin

    def _extract_image_paths(self, markdown_content: str) -> list[str]:
        """
        Extract image paths from markdown content.

        Args:
            markdown_content: The markdown text to parse

        Returns:
            List of image paths found in the document
        """
        # Match markdown image syntax: ![alt](path)
        image_pattern = r'!\[.*?\]\(([^)]+)\)'
        return re.findall(image_pattern, markdown_content)

    def _validate_images(self, markdown_content: str, base_dir: Path) -> None:
        """
        Validate that all referenced images exist.

        Args:
            markdown_content: The markdown text to check
            base_dir: Base directory for resolving relative paths

        Raises:
            FileNotFoundError: If any referenced image is missing
        """
        image_paths = self._extract_image_paths(markdown_content)
        missing_images = []

        for img_path in image_paths:
            # Skip URLs (http://, https://, data URIs, etc.)
            if img_path.startswith(("http://", "https://", "data:")):
                continue
            
            # Resolve relative to base directory
            resolved_path = base_dir / img_path
            if not resolved_path.exists():
                missing_images.append(img_path)

        if missing_images:
            raise FileNotFoundError(
                f"Missing image(s): {', '.join(missing_images)}. "
                f"Check that all image files exist relative to: {base_dir}"
            )

    def _apply_syntax_highlighting(self, markdown_content: str) -> str:
        """
        Apply syntax highlighting to fenced code blocks.

        Args:
            markdown_content: The markdown text to process

        Returns:
            Markdown with syntax-highlighted code blocks
        """
        # Pattern to match fenced code blocks: ```language\ncode\n```
        code_block_pattern = r"```(\w*\+?)\n(.*?)```"

        def replace_code_block(match: re.Match) -> str:
            language = match.group(1).strip().lower()
            code = match.group(2).strip()

            # Get lexer from explicit map (no dynamic loading)
            lexer_class = LEXER_MAP.get(language, TextLexer)
            lexer = lexer_class()

            # Highlight the code
            formatter = HtmlFormatter()
            highlighted = pygments.highlight(code, lexer, formatter)

            # Return as HTML block that will be preserved
            return f"\n\n{highlighted}\n\n"

        return re.sub(code_block_pattern, replace_code_block, markdown_content, flags=re.DOTALL)

    def convert_file(
        self, input_path: Path, output_path: Path, verbose: bool = False
    ) -> None:
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

        # Read the markdown content
        markdown_content = input_path.read_text(encoding="utf-8")
        file_size_kb = len(markdown_content.encode("utf-8")) / 1024

        if verbose:
            print(f"  Reading: {input_path} ({file_size_kb:.1f} KB)")

        # Validate that all referenced images exist
        self._validate_images(markdown_content, self.base_dir)

        if verbose:
            print("  Validating assets...")

        # Apply syntax highlighting to code blocks
        markdown_content = self._apply_syntax_highlighting(markdown_content)

        if verbose:
            print("  Applying syntax highlighting...")

        # Generate Pygments CSS for syntax highlighting
        pygments_css = HtmlFormatter().get_style_defs(".highlight")

        # Create section from the markdown file
        section = Section(
            markdown_content,
            toc=False,
            root=str(self.base_dir) if self.base_dir else ".",
            paper_size=self.page_size,
        )

        if verbose:
            print("  Generating PDF...")

        # Create PDF
        pdf = MarkdownPdf(
            toc_level=0,
            optimize=True,
        )
        pdf.add_section(section, user_css=pygments_css)

        # Save to file
        pdf.save(str(output_path))

        if verbose:
            output_size_kb = output_path.stat().st_size / 1024
            print(f"  Saved: {output_path} ({output_size_kb:.1f} KB)")
