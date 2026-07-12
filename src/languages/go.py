"""Go code formatter."""
import subprocess
from typing import Dict


class GoFormatter:
    """Format Go code using gofmt."""

    def format_file(self, filepath: str, check_only: bool = False) -> Dict:
        """Format a Go file.
        
        Args:
            filepath: Path to Go file
            check_only: If True, only check without modifying
            
        Returns:
            Result dictionary
        """
        result = {
            'file': filepath,
            'language': 'go',
            'success': False,
            'formatted': False,
            'error': None
        }

        try:
            if check_only:
                cmd = ['gofmt', '-l', filepath]
            else:
                cmd = ['gofmt', '-w', filepath]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode == 0:
                result['success'] = True
                result['formatted'] = not check_only and bool(proc.stdout.strip())
            else:
                result['error'] = proc.stderr

        except subprocess.TimeoutExpired:
            result['error'] = 'Formatting timed out'
        except FileNotFoundError:
            result['error'] = 'gofmt not installed'

        return result

    def get_config(self) -> Dict:
        """Get default Go formatting config."""
        return {}
