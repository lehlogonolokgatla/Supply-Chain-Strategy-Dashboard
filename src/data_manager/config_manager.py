# src/data_manager/config_manager.py
import json
from typing import Dict


class ConfigManager:
    def __init__(self, config_filepath: str):
        with open(config_filepath, 'r') as f:
            self.config = json.load(f)

    def get_variable_costs(self) -> Dict:
        return self.config['variable_costs']

    def get_param(self, category: str, key: str, default=None):
        return self.config.get(category, {}).get(key, default)