# Implementation Plan — md2pdf-cli

## Implementation Stack

- **Language**: Python 3.10+
- **PDF Engine**: `markdown-pdf` (PyMuPDF) - lightweight, no browser needed
- **CLI Framework**: `argparse` (stdlib)
- **Packaging**: PyInstaller for Windows .exe (~29MB, standalone)

---

## Task Checklist

### Phase 1: Project Setup

- [x] 1.1 Create `pyproject.toml` with project metadata and dependencies
- [x] 1.2 Set up virtual environment and install dependencies
- [x] 1.3 Create basic package structure (`src/md2pdf/`)
- [x] 1.4 Configure logging (for `--verbose` flag)

### Phase 2: Core Conversion Engine

- [x] 2.1 Implement Markdown → HTML converter module
  - [x] 2.1.1 Configure markdown extensions (tables, codehilite, etc.)
  - [x] 2.1.2 Add CSS injection support
- [x] 2.2 Implement HTML → PDF converter module
  - [x] 2.2.1 Integrate Playwright
  - [x] 2.2.2 Handle page size, margins via CSS
- [x] 2.3 Implement asset handling (image path resolution)
- [x] 2.4 Create default CSS template with proper fonts for Unicode

### Phase 3: CLI Implementation

- [x] 3.1 Implement CLI with `argparse`
  - [x] 3.1.1 Positional argument: `input` (markdown file)
  - [x] 3.1.2 Optional: `-o, --output` (output PDF path)
  - [x] 3.1.3 Optional: `--css` (custom CSS file)
  - [x] 3.1.4 Optional: `--page-size` (A4, Letter, etc.)
  - [x] 3.1.5 Optional: `--margin` (e.g., 10mm, 1in)
  - [x] 3.1.6 Optional: `--toc` (table of contents)
  - [x] 3.1.7 Optional: `--verbose` / `--quiet`
  - [x] 3.1.8 Optional: `--version` / `--help`
- [x] 3.2 Implement exit codes (0-5 per Requirements)
- [x] 3.3 Implement error handling with actionable messages

### Phase 4: Testing & Validation

- [x] 4.1 Create test document `testdata/sample.md`
  - [x] Include: headings, lists, blockquote, code block
  - [x] Include: basic table
  - [x] Include: embedded image (relative path)
  - [x] Include: Traditional Chinese text
- [x] 4.2 Add test image asset
- [x] 4.3 Manual test: verify PDF output
  - [x] Text selectable/copyable
  - [x] Unicode (Chinese) preserved
  - [x] Code blocks monospaced
  - [x] Images render correctly

### Phase 5: Distribution

- [x] 5.1 Windows: Build .exe with PyInstaller
- [ ] 5.2 Ubuntu: Document installation methods (pipx, pip)
- [x] 5.3 Create release artifacts (zip for Windows)

---

## Dependencies (pyproject.toml)

```toml
[project]
name = "md2pdf"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "markdown-pdf>=1.0",
    "requests>=2.0",  # Required by markdown-pdf for some features
]

[project.optional-dependencies]
dev = [
    "pyinstaller>=6.0",
]
```

---

## File Structure (Current)

```
md2pdf/
├── pyproject.toml
├── uv.lock
├── .venv/
├── src/md2pdf/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py          # CLI entry point
│   ├── converter.py    # Markdown → PDF (using markdown-pdf)
│   └── assets.py       # Image/path handling
├── testdata/
│   ├── sample.md
│   └── sample_new.pdf  # Generated output
├── dist/
│   ├── md2pdf.exe     # Standalone executable (~29MB)
│   └── md2pdf-win64.zip
├── project-documents/
│   ├── Requirements.md
│   └── ImplementationPlan.md
└── README.md
```

---

## Release Notes

- Switched from Playwright to markdown-pdf/PyMuPDF for much smaller executable size
- Original Playwright build: ~328MB
- New markdown-pdf build: ~29MB (91% smaller)
- No browser dependencies required
