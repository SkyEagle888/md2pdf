# Requirements.md — md2pdf-cli

## 1. Overview

### 1.1 Purpose

Build a small cross-platform command-line application that converts Markdown files into a PDF where the resulting PDF content is selectable and copyable as text (not rasterized).

### 1.2 Target users

- Windows 11 users who want a standalone `.exe` (no Python install required).
- Ubuntu Linux users who can run it via Python packaging or a Linux binary.

### 1.3 Key outcomes

- Fast, reliable Markdown → PDF conversion.
- Output PDFs must support copy/paste of text with correct Unicode (including Traditional Chinese).

## 2. In Scope (MVP)

### 2.1 Inputs

- A single Markdown file (`.md`) as input.
- Relative asset references:
  - Images (e.g., `./images/logo.png`)
  - Links (kept as clickable links in PDF if feasible)

### 2.2 Output

- A single PDF file (`.pdf`) generated from the input Markdown.
- PDF text must be selectable/copyable in common PDF viewers.

### 2.3 Markdown features (MVP)

- Headings (H1–H6)
- Paragraphs, emphasis (bold/italic), inline code
- Ordered/unordered lists
- Blockquotes
- Fenced code blocks (triple backticks) with **syntax highlighting** (300+ languages)
- Basic tables
- Images (embedded into the PDF)

### 2.4 Implementation stack (v0.1)

- **Language**: Python 3.10+
- **Markdown Parser**: `markdown-it-py` (via markdown-pdf)
- **PDF Engine**: `PyMuPDF` - lightweight, no browser needed
- **Syntax Highlighting**: `Pygments` - 33 language aliases via explicit lexer imports
- **Packaging**: PyInstaller for Windows `.exe` (~40MB, standalone)
- **Version Management**: `hatch-vcs` for automatic versioning from Git tags
- **Build Optimization**: Custom PyInstaller hook (`hooks/hook-pygments.py`) excludes unused lexers and heavy dependencies (numpy, scipy, pandas, matplotlib), reducing size from ~102MB to ~40MB

### 2.5 Rendering approach (implementation constraint for v0.1)

- Preferred pipeline: Markdown → HTML → PDF using a HTML-to-PDF engine that preserves real text.
- The produced PDF must not be made from screenshots of rendered pages.

## 3. Out of Scope (v0.1)

- Full GitHub-flavored Markdown parity if it adds complexity (task lists, footnotes, advanced tables).
- Mermaid diagrams rendering.
- LaTeX math rendering (unless it’s trivial to add).
- PDF forms, annotations, or digital signing.
- GUI application (CLI only).

## 4. CLI Requirements

### 4.1 Command name

- `md2pdf`

### 4.2 Basic usage

- `md2pdf input.md -o output.pdf`

### 4.3 CLI parameters (v0.1)

Required:

- `input`: Input markdown file path.

Optional:

- `-o, --output <path>`: Output PDF path (default: `<input_basename>.pdf` in same folder).
- `--page-size <A4|A3|A5|Letter|Legal|Tabloid>`: Page size preset (default: A4).
- `--margin <value>`: Page margin with format validation (e.g., `10mm`, `1in`, `2.5cm`).
- `--verbose`: Print debug logs and conversion progress.
- `--quiet`: Minimal output.
- `--version`: Print version.
- `--help`: Print help.

### 4.4 Exit codes

- `0`: Success.
- `1`: Generic failure.
- `2`: Invalid CLI usage / missing required args.
- `3`: Input file not found / unreadable.
- `4`: Conversion/render failure.
- `5`: Output path not writable.

## 5. Functional Requirements

### 5.1 Conversion correctness

- The tool must convert Markdown structure into PDF with readable formatting:
  - Headings are visually distinct.
  - Lists preserve nesting level (at least one level).
  - Code blocks are monospaced and do not collapse whitespace.

### 5.2 Copy/paste requirement (critical)

- Users must be able to select and copy text from the PDF and paste it into a text editor.
- Unicode must be preserved (English + Traditional Chinese at minimum).

### 5.3 Asset handling

- Images referenced via relative paths must render in the PDF.
- When an image is missing, the tool must:
  - Exit with code `3` (input file not found), and
  - Show a clear error message indicating which asset(s) failed to load.
  - Include the base directory path for reference.

### 5.4 Error messages

- Errors must be actionable:
  - Include which file/argument caused the problem.
  - Suggest a fix where reasonable (e.g., "check path", "install fonts").
  - For invalid margin format, list valid units (mm, cm, in, pt, px).
  - For conversion failures, suggest running with `--verbose` for details.
  - For permission errors, suggest checking write access to output directory.

## 6. Non-Functional Requirements

### 6.1 Cross-platform support

- Windows 11: distributable as a standalone `.exe`.
- Ubuntu Linux: runnable easily (via Python package entrypoint or Linux binary).

### 6.2 Distribution & packaging

Windows:

- Provide a single-file executable preferred (or a folder-based build if single-file is unreliable).
- End-user should not need to install Python.

Ubuntu:

- Provide a simple run method:
  - Option A: `pipx install ...` then run `md2pdf`
  - Option B: `python -m md2pdf ...`
  - Option C: downloadable Linux binary

### 6.3 Performance

- Should convert typical Markdown documents (e.g., 1–5 MB) in reasonable time on a standard laptop.
- Avoid excessive memory usage for typical documents.
- Provide progress feedback in verbose mode for large documents.
- **Executable size optimization**: Windows executable reduced from ~102MB to ~40MB by excluding unused Pygments lexers (200+) and heavy dependencies (numpy, scipy, pandas, matplotlib) via custom PyInstaller hook.

### 6.5 Progress indicator

- When `--verbose` is enabled, display step-by-step progress:
  - Reading input file (with file size)
  - Validating assets
  - Applying syntax highlighting
  - Generating PDF
  - Saving output file (with file size)

### 6.4 Determinism

- Given the same input files and same options, output should be consistent (excluding metadata like timestamps if included).

## 7. Acceptance Criteria (Definition of Done)

### 7.1 Test document

Create `testdata/sample.md` that includes:

- Headings, lists, blockquote
- Code block
- A table (if supported)
- An embedded image (relative path)
- Traditional Chinese text

### 7.2 Acceptance tests

- Running `md2pdf testdata/sample.md -o out.pdf` completes successfully with exit code `0`.
- Open `out.pdf` in a PDF viewer:
  - Text is selectable and copy/paste produces correct text (including Chinese).
  - Code blocks are readable, monospaced, and syntax-highlighted.
  - Images appear in the correct place.
- Windows 11:
  - `md2pdf.exe testdata\sample.md -o out.pdf` works on a machine without Python installed.
- Ubuntu:
  - The documented install/run method works on a clean environment.
- Error handling:
  - Missing image exits with code `3` and shows actionable error message.
  - Invalid margin format exits with code `2` and shows valid format examples.

## 8. Deliverables (v0.1)

- Source code
- `Requirements.md`
- `ImplementationPlan.md`
- `README.md` with usage examples
- Release artifacts:
  - Windows `.exe` (zip)
  - Ubuntu run method (instructions + optional binary)
- `testdata/sample.md` and required test assets (`testdata/images/logo.png`)
- `hooks/hook-pygments.py` - PyInstaller hook for minimizing executable size
