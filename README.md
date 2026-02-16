# md2pdf

A cross-platform CLI tool that converts Markdown to text-selectable PDFs (copy/paste friendly).

## Features

- **Selectable Text** - PDFs produced have real text, not rasterized images
- **Unicode Support** - Full support for English and Traditional Chinese
- **Markdown Support** - Headings, lists, blockquotes, code blocks, tables, images
- **Customizable** - CSS styling, page size, margins
- **Cross-Platform** - Windows (.exe) and Linux

## Installation

### Windows

Download the latest release from the [Releases](https://github.com/yourusername/md2pdf/releases) page.

### Linux

```bash
# Using pipx (recommended)
pipx install .

# Or using pip
pip install .
```

## Usage

```bash
# Basic conversion
md2pdf input.md -o output.pdf

# With custom CSS
md2pdf input.md --css custom.css -o output.pdf

# Change page size
md2pdf input.md --page-size Letter -o output.pdf

# Custom margins
md2pdf input.md --margin 20mm -o output.pdf

# Include table of contents
md2pdf input.md --toc -o output.pdf

# Verbose output
md2pdf input.md --verbose

# Quiet mode
md2pdf input.md --quiet
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Input markdown file (required) | - |
| `-o, --output` | Output PDF path | `<input_basename>.pdf` |
| `--css` | Custom CSS file | Built-in style |
| `--page-size` | Page size (A4, Letter, Legal, etc.) | A4 |
| `--margin` | Page margin (e.g., 10mm, 1in) | 10mm |
| `--toc` | Include table of contents | No |
| `--verbose` | Print debug logs | No |
| `--quiet` | Minimal output | No |
| `--version` | Show version | - |
| `--help` | Show help | - |

## Exit Codes

- `0` - Success
- `1` - Generic failure
- `2` - Invalid CLI usage
- `3` - Input file not found
- `4` - Conversion failure
- `5` - Output path not writable

## Requirements

- Windows .exe (no Python required)
- Python 3.10+ (for development/pip installation)

## License

MIT
