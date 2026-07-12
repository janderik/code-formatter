"""Python code formatter."""
import subprocess
import os
from typing import Dict


class PythonFormatter:
    """Format Python code using black and isort."""

    def format_file(self, filepath: str, check_only: bool = False) -> Dict:
        """Format a Python file.
        
        Args:
            filepath: Path to Python file
            check_only: If True, only check without modifying
            
        Returns:
            Result dictionary
        """
        result = {
            'file': filepath,
            'language': 'python',
            'success': False,
            'formatted': False,
            'error': None
        }

        try:
            # Run black
            cmd = ['python', '-m', 'black']
            if check_only:
                cmd.append('--check')
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

            # Run isort
            isort_cmd = ['python', '-m', 'isort']
            if check_only:
                isort_cmd.append('--check-only')
            isort_cmd.append(filepath)

            subprocess.run(
                isort_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

        except subprocess.TimeoutExpired:
            result['error'] = 'Formatting timed out'
        except FileNotFoundError:
            result['error'] = 'black or isort not installed'

        return result

    def get_config(self) -> Dict:
        """Get default Python formatting config."""
        return {
            'line_length': 88,
            'target_version': 'py38',
            'skip_string_normalization': False,
        }
