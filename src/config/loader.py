"""Configuration loader."""
import os
import json
import yaml
from typing import Dict, Any


class ConfigLoader:
    """Load and merge configuration files."""

    DEFAULT_CONFIG = {
        'line_ending': 'auto',
        'encoding': 'utf-8',
        'max_line_length': 88,
        'ignore': [
            'node_modules',
            'venv',
            '__pycache__',
            '.git',
            'vendor',
            '*.min.js',
            '*.min.css',
        ],
        'languages': {}
    }

    CONFIG_FILES = [
        '.fmtconfig.yaml',
        '.fmtconfig.yml',
        '.fmtconfig.json',
        '.formatterconfig',
    ]

    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._find_config_file()

    def _find_config_file(self) -> str:
        """Find configuration file in current directory."""
        for filename in self.CONFIG_FILES:
            if os.path.exists(filename):
                return filename
        return None

    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        config = self.DEFAULT_CONFIG.copy()

        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    if self.config_file.endswith('.json'):
                        file_config = json.load(f)
                    else:
                        file_config = yaml.safe_load(f) or {}

                config = self._merge_configs(config, file_config)
            except Exception as e:
                print(f"Warning: Failed to load config {self.config_file}: {e}")

        return config

    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """Merge two configuration dictionaries."""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def save(self, config: Dict[str, Any], filepath: str = None):
        """Save configuration to file."""
        filepath = filepath or self.config_file or '.fmtconfig.yaml'

        with open(filepath, 'w') as f:
            if filepath.endswith('.json'):
                json.dump(config, f, indent=2)
            else:
                yaml.dump(config, f, default_flow_style=False)
