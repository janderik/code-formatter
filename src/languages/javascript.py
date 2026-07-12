"""JavaScript/TypeScript code formatter."""
import subprocess
from typing import Dict


class JavaScriptFormatter:
    """Format JavaScript/TypeScript code using prettier."""

    def format_file(self, filepath: str, check_only: bool = False) -> Dict:
        """Format a JavaScript/TypeScript file.
        
        Args:
            filepath: Path to JS/TS file
            check_only: If True, only check without modifying
            
        Returns:
            Result dictionary
        """
        result = {
            'file': filepath,
            'language': 'javascript',
            'success': False,
            'formatted': False,
            'error': None
        }

        try:
            cmd = ['npx', 'prettier', '--write']
            if check_only:
                cmd = ['npx', 'prettier', '--check']
            cmd.append(filepath)

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if proc.returncode == 0:
                result['success'] = True
                result['formatted'] = not check_only
            else:
                result['error'] = proc.stderr

        except subprocess.TimeoutExpired:
            result['error'] = 'Formatting timed out'
        except FileNotFoundError:
            result['error'] = 'prettier not installed'

        return result

    def get_config(self) -> Dict:
        """Get default JavaScript formatting config."""
        return {
            'print_width': 100,
            'tab_width': 2,
            'use_tabs': False,
            'semi': True,
            'single_quote': False,
            'trailing_comma': 'all',
            'bracket_spacing': True,
        }
