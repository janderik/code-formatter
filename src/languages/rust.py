"""Rust code formatter."""
import subprocess
from typing import Dict


class RustFormatter:
    """Format Rust code using rustfmt."""

    def format_file(self, filepath: str, check_only: bool = False) -> Dict:
        """Format a Rust file.
        
        Args:
            filepath: Path to Rust file
            check_only: If True, only check without modifying
            
        Returns:
            Result dictionary
        """
        result = {
            'file': filepath,
            'language': 'rust',
            'success': False,
            'formatted': False,
            'error': None
        }

        try:
            if check_only:
                cmd = ['rustfmt', '--check', filepath]
            else:
                cmd = ['rustfmt', filepath]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode == 0:
                result['success'] = True
                result['formatted'] = not check_only
            else:
                result['error'] = proc.stderr

        except subprocess.TimeoutExpired:
            result['error'] = 'Formatting timed out'
        except FileNotFoundError:
            result['error'] = 'rustfmt not installed'

        return result

    def get_config(self) -> Dict:
        """Get default Rust formatting config."""
        return {
            'max_width': 100,
            'tab_spaces': 4,
            'use_small_heuristics': 'Default',
        }
