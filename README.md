# md2pdf

A cross-platform CLI tool that converts Markdown to text-selectable, copy/paste-friendly PDFs.

![Version](https://img.shields.io/badge/version-0.1-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

## Features

- **Selectable Text** — PDFs contain real text, not rasterized images. Copy/paste works perfectly.
- **Syntax Highlighting** — Automatic code highlighting for 300+ languages via Pygments.
- **Unicode Support** — Full support for English and Traditional Chinese characters.
- **Smart Validation** — Checks for missing images before conversion with clear error messages.
- **Progress Indicator** — Step-by-step feedback in verbose mode.
- **Cross-Platform** — Standalone Windows .exe (~40MB) and Python package for Linux.
- **Context Menu** — Right-click `.md` files to convert (Windows 11).
- **Customizable** — Page size, margins, and output control.

## Installation

### Windows

Download the latest release from the [Releases](https://github.com/SkyEagle888/md2pdf/releases) page:

1. Download `md2pdf-win64.zip`
2. Extract to a folder (e.g., `C:\Program Files\md2pdf`)
3. Add the folder to your `PATH` environment variable
4. Run from anywhere:
   ```powershell
   md2pdf input.md -o output.pdf
   ```

**No Python installation required.**

#### Windows 11 Context Menu (Optional)

Right-click on any `.md` file to convert it directly:

1. **Copy files to your installation folder** (e.g., `C:\Program Files\md2pdf`):
   - `dist/md2pdf.exe` - The main executable
   - `assets/md2pdf.bat` - Batch wrapper for context menu

2. **Edit `md2pdf.bat`** - Update the path to match your installation:
   ```batch
   C:\Program Files\md2pdf\dist\md2pdf.exe %filename% --skip-validation
   ```

3. **Edit `md2pdf-windows.reg`** - Update both paths to match your installation

4. **Register the context menu** (Run as Administrator):
   ```powershell
   # Delete old entries (if any)
   reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Convert to PDF" /f
   
   # Merge the new registry
   reg import C:\Program Files\md2pdf\assets\md2pdf-windows.reg
   ```

5. **Restart Windows Explorer** (or log out/in)

6. **Right-click any `.md` file** → **"Show more options"** → **"Convert to PDF"**

> **Note:** On Windows 11, the menu appears under "Show more options" by design.  
> **Tip:** Use `Shift + Right-click` to open the extended menu directly.  
> **Note:** The `--skip-validation` flag is auto-added to handle README files with missing images.

### Linux

```bash
# Using pipx (recommended - isolates the tool)
pipx install .

# Or using pip (installs to current environment)
pip install .

# Then run from anywhere
md2pdf input.md -o output.pdf
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/md2pdf.git
cd md2pdf

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install with dev dependencies
pip install -e ".[dev]"

# Run from source
python -m md2pdf input.md -o output.pdf
```

## Usage

### Basic Conversion

```bash
# Convert with default output (input.pdf)
md2pdf document.md

# Specify output file
md2pdf document.md -o report.pdf
```

### Page Layout

```bash
# Custom page size
md2pdf document.md --page-size Letter -o output.pdf

# Custom margins (supports mm, cm, in, pt, px)
md2pdf document.md --margin 20mm -o output.pdf
md2pdf document.md --margin 1in -o output.pdf
```

### Output Control

```bash
# Verbose mode - shows progress and debug info
md2pdf document.md --verbose

# Quiet mode - minimal output
md2pdf document.md --quiet

# Check version
md2pdf --version
```

### Full Example

```bash
md2pdf readme.md \
  --page-size A4 \
  --margin 15mm \
  --verbose \
  -o readme.pdf
```

## CLI Options

| Option | Description | Default | Notes |
|--------|-------------|---------|-------|
| `input` | Input markdown file | **Required** | Must exist |
| `-o, --output` | Output PDF path | `<input>.pdf` | Parent dir must be writable |
| `--page-size` | Page size preset | `A4` | A4, A3, A5, Letter, Legal, Tabloid |
| `--margin` | Page margin | `10mm` | Format: `<number><unit>` (e.g., `10mm`, `1in`) |
| `--verbose` | Show progress and debug logs | Off | Recommended for large files |
| `--quiet` | Minimal output | Off | Mutually exclusive with `--verbose` |
| `--skip-validation` | Skip image validation | Off | Useful for READMEs with missing images |
| `--version` | Show version number | — | — |
| `--help` | Show help message | — | — |

### Margin Format

Valid units: `mm`, `cm`, `in`, `pt`, `px`

Examples:
- `10mm` — 10 millimeters
- `1in` — 1 inch
- `2.5cm` — 2.5 centimeters
- `72pt` — 72 points
- `96px` — 96 pixels

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| `0` | Success | PDF created successfully |
| `1` | Generic failure | Unexpected error |
| `2` | Invalid CLI usage | Invalid margin format, missing arguments |
| `3` | Input file not found | Markdown file or referenced image missing |
| `4` | Conversion failure | PDF generation error |
| `5` | Output not writable | Permission denied on output path |

## Progress Indicator

When `--verbose` is enabled, you'll see step-by-step progress:

```
Reading: document.md (2.4 KB)
  Validating assets...
  Applying syntax highlighting...
  Generating PDF...
  Saved: output.pdf (156.3 KB)
```

## Supported Markdown Features

- **Headings** — H1 through H6
- **Text formatting** — Bold, italic, inline code
- **Lists** — Ordered and unordered (nested)
- **Blockquotes**
- **Code blocks** — Fenced with triple backticks, syntax-highlighted
- **Tables** — Basic Markdown tables
- **Images** — Embedded via relative paths
- **Links** — Preserved as clickable in PDF

## Syntax Highlighting

Code blocks are automatically highlighted using [Pygments](https://pygments.org/), supporting 300+ languages:

````markdown
```python
def hello():
    print("Hello, world!")
```

```typescript
const greet = (name: string) => `Hello, ${name}!`;
```

```rust
fn main() {
    println!("Hello, world!");
}
```
````

Specify the language after the opening backticks for best results. If omitted, the block will render without highlighting.

## Image Handling

Images referenced with relative paths are embedded in the PDF:

```markdown
![Logo](./images/logo.png)
```

**Validation:** Before conversion, md2pdf checks that all referenced images exist. If an image is missing:

```
Error: Image not found: ./images/logo.png
Base directory: C:\Projects\document\
Exit code: 3
```

## Examples

### README to PDF

```bash
md2pdf README.md --page-size A4 --margin 15mm -o README.pdf
```

### Report with Chinese Text

```bash
md2pdf report-zh.md --verbose -o report.pdf
```

### Debug Conversion Issues

```bash
md2pdf complex.md --verbose -o complex.pdf
```

## Build from Source

### Prerequisites

- Python 3.10+
- pip or uv

### Build Steps

```bash
# Install dependencies
pip install -e ".[dev]"

# Build Windows executable with embedded icon
# Excludes numpy, scipy, pandas to reduce size from 102MB to ~40MB
pyinstaller --onefile --name md2pdf \
  --icon=assets/md2pdf-logo-1.ico \
  --additional-hooks-dir=./hooks \
  --exclude-module numpy \
  --exclude-module scipy \
  --exclude-module pandas \
  --exclude-module matplotlib \
  src/md2pdf/__main__.py

# Output: dist/md2pdf.exe (~40MB with embedded icon)
```

**Note:** The build uses a custom PyInstaller hook (`hooks/hook-pygments.py`) that includes only commonly-used language lexers (Python, JavaScript, TypeScript, Bash, JSON, YAML, etc.) and excludes 200+ unused lexers. Heavy dependencies (numpy, scipy, pandas, matplotlib) are explicitly excluded as they are not needed by md2pdf.

### Project Structure

```
md2pdf/
├── src/md2pdf/
│   ├── __init__.py      # Package init, version import
│   ├── __main__.py      # Entry point
│   ├── cli.py           # CLI argument parsing
│   ├── converter.py     # Markdown → PDF conversion (with explicit lexer imports)
│   └── assets.py        # Image path resolution
├── testdata/
│   ├── sample.md        # Test document
│   └── images/
│       └── logo.png     # Test image
├── hooks/
│   └── hook-pygments.py # PyInstaller hook to minimize Pygments footprint
├── assets/
│   ├── md2pdf-logo-1.ico    # Windows icon for .exe
│   ├── md2pdf-logo-1.png    # Logo image
│   ├── md2pdf-logo-2.png    # Logo image
│   └── md2pdf-windows.reg   # Windows 11 context menu registry
├── project-documents/
│   ├── Requirements.md
│   └── ImplementationPlan.md
└── pyproject.toml
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| PDF Engine | markdown-pdf (PyMuPDF) |
| CLI Framework | argparse (stdlib) |
| Syntax Highlighting | Pygments |
| Packaging | PyInstaller (Windows), pip/pipx (Linux) |
| Versioning | hatch-vcs (Git tag-based) |

## Troubleshooting

### "Image not found" error

Ensure image paths are relative to the markdown file's directory:

```markdown
<!-- If document.md is in /docs/, reference images like: -->
![Logo](./images/logo.png)
```

### "Invalid margin format" error

Use the format `<number><unit>` with no space:

```bash
# ✓ Correct
--margin 10mm
--margin 1in

# ✗ Incorrect
--margin 10 mm
--margin "10 mm"
```

### Permission denied on output

Check that the output directory exists and is writable:

```bash
# Create directory first if needed
mkdir -p ./output
md2pdf input.md -o ./output/file.pdf
```

## License

MIT License — see [LICENSE](LICENSE) for details.
