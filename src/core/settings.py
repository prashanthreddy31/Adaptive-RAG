"""
Configuation settings for the application
"""

import os
from pathlib import Path
import yaml

class Config:
    """Load and manage configurations from yaml file"""

    def __init__(self, config_file:str = None):
        """
        Initialize configuration from YAML file.

        Args:
            config_file: Optional path to config file. Defaults to prompts.yaml.
        """
        base_path = Path(__file__).parent
        config_path = (
            base_path/"prompts.yaml"
            if config_file is None
            else Path(config_file)
        )        
        with open(config_path, 'r') as p:
            self.config = yaml.safe_load(p)

    def prompt(self, key: str) -> str:
        """
        Retrieve a prompt from configuration.

        Args:
            key: The prompt key.

        Returns:
            The prompt template string.
        """
        return self.config["prompts"][key]

