# md2pdf

A cross-platform CLI tool that converts Markdown to text-selectable PDFs (copy/paste friendly).

## Features

- **Selectable Text** - PDFs produced have real text, not rasterized images
- **Unicode Support** - Full support for English and Traditional Chinese
- **Syntax Highlighting** - Automatic code highlighting for 300+ languages
- **Markdown Support** - Headings, lists, blockquotes, code blocks, tables, images
- **Customizable** - Page size, margins, verbose output
- **Cross-Platform** - Windows (.exe) and Linux
- **Smart Validation** - Checks for missing images before conversion

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

# With custom page size
md2pdf input.md --page-size Letter -o output.pdf

# Custom margins
md2pdf input.md --margin 20mm -o output.pdf

# Verbose output (shows progress)
md2pdf input.md --verbose

# Quiet mode
md2pdf input.md --quiet
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Input markdown file (required) | - |
| `-o, --output` | Output PDF path | `<input_basename>.pdf` |
| `--page-size` | Page size (A4, Letter, Legal, etc.) | A4 |
| `--margin` | Page margin (e.g., 10mm, 1in, 2cm) | 10mm |
| `--verbose` | Print debug logs and progress | No |
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
