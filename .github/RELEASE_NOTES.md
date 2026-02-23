# Release Notes

## v0.1.2 (2026-02-23)

### 🎉 Windows Context Menu Integration

#### Registry File for Right-Click Conversion
- **Updated `md2pdf-windows.reg`** for Windows 11 context menu integration
- Right-click on any `.md` file → "Convert to PDF"
- Assumes `md2pdf.exe` is in your `PATH` environment variable
- Uses embedded icon from the executable (no external .ico file needed)

#### How to Use
1. Add the `dist` folder to your PATH environment variable
2. Double-click `assets/md2pdf-windows.reg` to register the context menu
3. Right-click any `.md` file and select "Convert to PDF"

#### Registry Details
```reg
[HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Convert to PDF]
@="Convert to PDF"
"Icon"="md2pdf.exe"

[HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Convert to PDF\command]
@="\"md2pdf.exe\" \"%1\""
```

---

## v0.1.1 (2026-02-17)

### 🎉 Major Improvements

#### Build Optimization - 61% Size Reduction!
- **Windows executable reduced from 102MB to ~40MB**
- Custom PyInstaller hook (`hooks/hook-pygments.py`) excludes 200+ unused Pygments lexers
- Explicit lexer imports for 33 common language aliases (no dynamic loading)
- Excluded heavy dependencies: numpy, scipy, pandas, matplotlib

### 🔧 Technical Changes

#### Syntax Highlighting
- Replaced dynamic `get_lexer_by_name()` with explicit lexer imports
- Added `LEXER_MAP` with 33 language aliases:
  - **Python**: python, py
  - **JavaScript/TypeScript**: javascript, js, typescript, ts
  - **Shell**: bash, sh, shell, zsh, powershell, ps1, pwsh
  - **Data formats**: json, yaml, yml
  - **Web**: html, xml, css
  - **System languages**: go, rust, c, cpp, c++
  - **Java ecosystem**: java, kotlin, scala
  - **Config files**: ini, toml
  - **Markup**: markdown, md
  - **Database**: sql
  - **Other**: diff

#### Build Command
```bash
pyinstaller --onefile --name md2pdf \
  --additional-hooks-dir=./hooks \
  --exclude-module numpy \
  --exclude-module scipy \
  --exclude-module pandas \
  --exclude-module matplotlib \
  src/md2pdf/__main__.py
```

### 📚 Documentation Updates
- Updated README.md with optimized build instructions
- Revised Requirements.md to reflect current implementation
- Updated ImplementationPlan.md with completed optimization tasks

---

## v0.1.0 (2026-02-16)

### 🚀 Initial Release

A cross-platform CLI tool that converts Markdown to text-selectable, copy/paste-friendly PDFs.

#### Features
- **Selectable Text** — PDFs contain real text, not rasterized images
- **Syntax Highlighting** — Automatic code highlighting via Pygments
- **Unicode Support** — Full support for English and Traditional Chinese
- **Smart Validation** — Checks for missing images before conversion
- **Progress Indicator** — Step-by-step feedback in verbose mode
- **Cross-Platform** — Windows .exe and Python package for Linux

#### Installation
- **Windows**: Download `md2pdf-win64.zip` from Releases
- **Linux**: `pipx install md2pdf` or `pip install md2pdf`

#### Usage
```bash
md2pdf input.md -o output.pdf
md2pdf README.md --page-size A4 --margin 15mm -o README.pdf
```

#### Technology Stack
- Language: Python 3.10+
- PDF Engine: markdown-pdf (PyMuPDF)
- Syntax Highlighting: Pygments
- Packaging: PyInstaller (Windows), pip/pipx (Linux)
