# md2pdf v0.1.0 Release Notes

## What's New

This release includes significant improvements to md2pdf:

### Features

- **Syntax Highlighting**: Automatic code highlighting for 300+ languages using Pygments
- **Image Validation**: Checks for missing images before conversion, fails fast with clear error messages
- **Margin Format Validation**: Validates margin format (e.g., `10mm`, `1in`, `2.5cm`)
- **Progress Indicator**: Verbose mode shows step-by-step conversion progress
- **Automatic Versioning**: Version managed by hatch-vcs from Git tags
- **Improved Error Messages**: Actionable errors with helpful tips

### Breaking Changes

- Removed `--css` option (not supported by markdown-pdf)
- Removed `--toc` option (not implemented)

### Installation

#### Windows

Download `md2pdf-win64.zip` from the assets below, extract, and run `md2pdf.exe`.

#### Linux/macOS

```bash
pip install md2pdf
# or
pipx install md2pdf
```

### Usage

```bash
# Basic conversion
md2pdf input.md -o output.pdf

# With custom page size
md2pdf input.md --page-size Letter -o output.pdf

# Custom margins
md2pdf input.md --margin 20mm -o output.pdf

# Verbose output (shows progress)
md2pdf input.md --verbose
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic failure |
| 2 | Invalid CLI usage |
| 3 | Input file not found (including missing images) |
| 4 | Conversion failure |
| 5 | Output path not writable |

### Technical Details

- **Executable Size**: ~40 MB (standalone, no Python required)
- **Python Version**: 3.10+
- **PDF Engine**: markdown-pdf (PyMuPDF)
- **Syntax Highlighting**: Pygments (common languages)

### Full Changelog

[See all changes](https://github.com/SkyEagle888/md2pdf/compare/ea4dcd5...d6d44b6)
