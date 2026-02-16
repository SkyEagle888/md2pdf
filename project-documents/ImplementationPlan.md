# Implementation Plan — md2pdf-cli

## Implementation Stack

- **Language**: Python 3.10+
- **PDF Engine**: `markdown-pdf` (PyMuPDF) - lightweight, no browser needed
- **CLI Framework**: `argparse` (stdlib)
- **Syntax Highlighting**: `Pygments` - 300+ language support
- **Packaging**: PyInstaller for Windows .exe (~29MB, standalone)
- **Version Management**: `hatch-vcs` for automatic versioning from Git tags

---

## Task Checklist

### Phase 1: Project Setup

- [x] 1.1 Create `pyproject.toml` with project metadata and dependencies
- [x] 1.2 Set up virtual environment and install dependencies
- [x] 1.3 Create basic package structure (`src/md2pdf/`)
- [x] 1.4 Configure logging (for `--verbose` flag)

### Phase 2: Core Conversion Engine

- [x] 2.1 Implement Markdown → PDF converter module
  - [x] 2.1.1 Configure markdown parsing (tables, fenced code blocks)
  - [x] 2.1.2 Add syntax highlighting with Pygments
- [x] 2.2 Implement HTML → PDF converter module
  - [x] 2.2.1 Integrate markdown-pdf/PyMuPDF
  - [x] 2.2.2 Handle page size, margins via CSS
  - [x] 2.2.3 Inject Pygments CSS for code highlighting
- [x] 2.3 Implement asset handling (image path resolution)
  - [x] 2.3.1 Extract image paths from markdown
  - [x] 2.3.2 Validate image existence before conversion
- [x] 2.4 Create test image asset (`testdata/images/logo.png`)

### Phase 3: CLI Implementation

- [x] 3.1 Implement CLI with `argparse`
  - [x] 3.1.1 Positional argument: `input` (markdown file)
  - [x] 3.1.2 Optional: `-o, --output` (output PDF path)
  - [x] 3.1.3 Optional: `--page-size` (A4, A3, A5, Letter, Legal, Tabloid)
  - [x] 3.1.4 Optional: `--margin` (with format validation)
  - [x] 3.1.5 Optional: `--verbose` / `--quiet`
  - [x] 3.1.6 Optional: `--version` / `--help`
- [x] 3.2 Implement exit codes (0-5 per Requirements)
- [x] 3.3 Implement error handling with actionable messages
  - [x] 3.3.1 Missing image detection
  - [x] 3.3.2 Invalid margin format validation
  - [x] 3.3.3 Permission error handling
  - [x] 3.3.4 Verbose mode tips

### Phase 4: Testing & Validation

- [x] 4.1 Create test document `testdata/sample.md`
  - [x] Include: headings, lists, blockquote, code block
  - [x] Include: basic table
  - [x] Include: embedded image (relative path)
  - [x] Include: Traditional Chinese text
- [x] 4.2 Add test image asset (`testdata/images/logo.png`)
- [x] 4.3 Manual test: verify PDF output
  - [x] Text selectable/copyable
  - [x] Unicode (Chinese) preserved
  - [x] Code blocks syntax-highlighted
  - [x] Images render correctly
- [x] 4.4 Test error scenarios
  - [x] Missing image → exit code 3
  - [x] Invalid margin → exit code 2
  - [x] Version command works

### Phase 5: Distribution

- [x] 5.1 Windows: Build .exe with PyInstaller
- [ ] 5.2 Ubuntu: Document installation methods (pipx, pip)
- [x] 5.3 Create release artifacts (zip for Windows)
- [x] 5.4 Configure automatic versioning with hatch-vcs

---

## Dependencies (pyproject.toml)

```toml
[project]
name = "md2pdf"
dynamic = ["version"]
requires-python = ">=3.10"

dependencies = [
    "markdown-pdf>=1.0",
    "pygments>=2.0",
]

[project.optional-dependencies]
dev = [
    "pyinstaller>=6.0",
    "hatch-vcs>=0.4",
]

[project.scripts]
md2pdf = "md2pdf.cli:main"

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"
```

---

## File Structure (Current)

```
md2pdf/
├── pyproject.toml
├── uv.lock
├── .venv/
├── src/md2pdf/
│   ├── __init__.py         # Dynamic version import
│   ├── __main__.py         # Package entry point
│   ├── cli.py              # CLI entry point with argparse
│   ├── converter.py        # Markdown → PDF (markdown-pdf + Pygments)
│   └── assets.py           # Image path resolution
├── testdata/
│   ├── sample.md           # Test document
│   └── images/
│       └── logo.png        # Test image asset
├── dist/
│   ├── md2pdf.exe          # Standalone executable (~29MB)
│   └── md2pdf-win64.zip
├── project-documents/
│   ├── Requirements.md
│   └── ImplementationPlan.md
└── README.md
```

---

## CLI Options (Final)

| Option | Description | Default | Validation |
|--------|-------------|---------|------------|
| `input` | Input markdown file (required) | - | File must exist |
| `-o, --output` | Output PDF path | `<input_basename>.pdf` | Parent dir must be writable |
| `--page-size` | Page size | A4 | A4, A3, A5, Letter, Legal, Tabloid |
| `--margin` | Page margin | 10mm | Format: `<number><unit>` (mm, cm, in, pt, px) |
| `--verbose` | Debug logs and progress | No | - |
| `--quiet` | Minimal output | No | - |
| `--version` | Show version | - | - |
| `--help` | Show help | - | - |

**Removed options:**
- `--css` - Removed (not supported by markdown-pdf)
- `--toc` - Removed (not implemented)

---

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| 0 | Success | PDF created successfully |
| 1 | Generic failure | Unexpected error |
| 2 | Invalid CLI usage | Invalid margin format, missing args |
| 3 | Input file not found | Markdown file or image missing |
| 4 | Conversion failure | PDF generation error |
| 5 | Output not writable | Permission denied |

---

## Key Features Implemented

### Syntax Highlighting
- Automatic language detection for code blocks
- Support for 300+ languages via Pygments
- CSS injected into PDF for proper styling

### Image Validation
- Scans markdown for `![alt](path)` patterns
- Validates all images exist before conversion
- Clear error message with missing file paths

### Margin Validation
- Regex pattern: `^\d+(\.\d+)?(mm|cm|in|pt|px)$`
- Examples: `10mm`, `1in`, `2.5cm`, `72pt`
- Helpful error message with valid formats

### Progress Indicator (--verbose)
```
Reading: input.md (0.8 KB)
  Validating assets...
  Applying syntax highlighting...
  Generating PDF...
  Saved: output.pdf (2157.6 KB)
```

### Version Management
- Automatic versioning from Git tags via `hatch-vcs`
- Format: `0.1.dev3+gea4dcd531.d20260216`
- No manual version updates needed

---

## Release Notes

### v0.1 (Current)
- Switched from Playwright to markdown-pdf/PyMuPDF for smaller executable
  - Original Playwright build: ~328MB
  - New markdown-pdf build: ~29MB (91% smaller)
- No browser dependencies required
- Added syntax highlighting with Pygments
- Added image validation before conversion
- Added margin format validation
- Implemented automatic versioning with hatch-vcs
- Removed unsupported options: `--css`, `--toc`
- Enhanced error messages with actionable tips
- Added progress indicator in verbose mode

---

## Future Enhancements (Backlog)

- [ ] Unit tests with pytest
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] PyPI publishing for `pipx install md2pdf`
- [ ] Custom CSS support (if markdown-pdf adds feature)
- [ ] Table of contents generation
- [ ] Mermaid diagram rendering
- [ ] LaTeX math support
