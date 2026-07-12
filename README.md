# code-formatter

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![PyPI Version](https://img.shields.io/badge/PyPI-v1.0.0-orange)]()
[![Downloads](https://img.shields.io/badge/downloads-12K+-blue)]()

A multi-language code formatter supporting Python, JavaScript, TypeScript, Go, Rust, and more with configurable formatting rules and editor integration.

## Features

- Multi-language support (Python, JS, TS, Go, Rust, Java, C/C++)
- Configurable formatting rules
- Editor integration (VS Code, Vim, Emacs)
- Pre-commit hook support
- CI/CD integration
- Batch formatting
- Diff preview mode
- EditorConfig support
- Custom formatters

## Supported Languages

| Language | Formatter | Config File |
|----------|-----------|-------------|
| Python | black, isort | pyproject.toml |
| JavaScript | prettier | .prettierrc |
| TypeScript | prettier | .prettierrc |
| Go | gofmt | - |
| Rust | rustfmt | rustfmt.toml |
| Java | google-java-format | - |
| C/C++ | clang-format | .clang-format |
| HTML | prettier | .prettierrc |
| CSS | prettier | .prettierrc |
| JSON | prettier | .prettierrc |
| YAML | prettier | .prettierrc |
| Markdown | prettier | .prettierrc |

## Architecture

```
code-formatter/
├── src/
│   ├── formatter/        # Core formatting engine
│   │   ├── __init__.py
│   │   ├── engine.py     # Main formatter
│   │   └── runner.py     # Process runner
│   ├── languages/        # Language-specific formatters
│   │   ├── __init__.py
│   │   ├── python.py
│   │   ├── javascript.py
│   │   ├── go.py
│   │   └── rust.py
│   └── config/           # Configuration system
│       ├── __init__.py
│       ├── loader.py
│       └── defaults.py
├── cli.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Installation

### From PyPI

```bash
pip install code-formatter
```

### From Source

```bash
git clone https://github.com/janderik/code-formatter.git
cd code-formatter
pip install -e .
```

## Usage

### Basic Usage

```bash
# Format a file
fmt src/main.py

# Format multiple files
fmt src/*.py

# Format entire directory
fmt src/

# Check without modifying (dry run)
fmt --check src/
```

### Configuration

Create `.fmtconfig.yaml`:

```yaml
languages:
  python:
    formatter: black
    options:
      line-length: 88
      target-version: py38
  javascript:
    formatter: prettier
    options:
      print-width: 100
      single-quote: true
      trailing-comma: all
  go:
    formatter: gofmt
  rust:
    formatter: rustfmt

ignore:
  - node_modules
  - venv
  - __pycache__
  - "*.min.js"
  - vendor
```

### Config Options

```yaml
# Global options
line-ending: auto  # auto, lf, crlf
encoding: utf-8
max-line-length: 88

# Language-specific options
languages:
  python:
    formatter: black
    options:
      line-length: 88
      skip-string-normalization: false
      target-version: py38

  javascript:
    formatter: prettier
    options:
      print-width: 100
      tab-width: 2
      use-tabs: false
      semi: true
      single-quote: false
      trailing-comma: all
      bracket-spacing: true
      arrow-parens: always
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: code-formatter
        name: Code Formatter
        entry: fmt
        language: system
        types: [python, javascript, typescript, go, rust]
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Format code
  uses: janderik/code-formatter-action@v1
  with:
    check: true
    format: true

# GitLab CI
format:
  script:
    - fmt --check .
```

### Editor Integration

#### VS Code

Add to `settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "janderik.code-formatter"
}
```

#### Vim/Neovim

```vim
autocmd BufWritePre *.py :!fmt %
autocmd BufWritePre *.js,*.ts :!fmt %
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
