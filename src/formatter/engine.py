"""Main code formatting engine."""
import os
import subprocess
from typing import List, Dict, Optional
from ..config.loader import ConfigLoader
from ..languages.python import PythonFormatter
from ..languages.javascript import JavaScriptFormatter
from ..languages.go import GoFormatter
from ..languages.rust import RustFormatter


class CodeFormatter:
    """Main code formatter supporting multiple languages."""

    LANGUAGE_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
    }

    def __init__(self, config_file: str = None):
        self.config = ConfigLoader(config_file).load()
        self.formatters = {
            'python': PythonFormatter(),
            'javascript': JavaScriptFormatter(),
            'typescript': JavaScriptFormatter(),
            'go': GoFormatter(),
            'rust': RustFormatter(),
        }
        self.results: List[Dict] = []

    def format_path(self, path: str, check_only: bool = False) -> List[Dict]:
        """Format a file or directory.
        
        Args:
            path: File or directory to format
            check_only: If True, only check without modifying
            
        Returns:
            List of formatting results
        """
        self.results = []

        if os.path.isfile(path):
            self._format_file(path, check_only)
        elif os.path.isdir(path):
            self._format_directory(path, check_only)

        return self.results

    def _format_file(self, filepath: str, check_only: bool = False):
        """Format a single file."""
        ext = os.path.splitext(filepath)[1].lower()
        language = self.LANGUAGE_MAP.get(ext)

        if not language:
            return

        formatter = self.formatters.get(language)
        if not formatter:
            return

        # Check ignore patterns
        if self._should_ignore(filepath):
            return

        try:
            result = formatter.format_file(filepath, check_only)
            self.results.append(result)
        except Exception as e:
            self.results.append({
                'file': filepath,
                'success': False,
                'error': str(e)
            })

    def _format_directory(self, directory: str, check_only: bool = False):
        """Format all files in a directory."""
        ignore_dirs = self.config.get('ignore', [])
        ignore_dirs.extend(['node_modules', '.git', 'venv', '__pycache__', 'vendor'])

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for filename in files:
                filepath = os.path.join(root, filename)
                self._format_file(filepath, check_only)

    def _should_ignore(self, filepath: str) -> bool:
        """Check if file should be ignored."""
        ignore_patterns = self.config.get('ignore', [])
        basename = os.path.basename(filepath)

        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                if basename.endswith(pattern[1:]):
                    return True
            elif basename == pattern:
                return True

        return False

    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return list(self.LANGUAGE_MAP.keys())

    def get_language(self, filepath: str) -> Optional[str]:
        """Get language for a file."""
        ext = os.path.splitext(filepath)[1].lower()
        return self.LANGUAGE_MAP.get(ext)
