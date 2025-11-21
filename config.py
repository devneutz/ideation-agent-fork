"""
Configuration management for the Ideation Agent
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for managing API keys and settings."""

    def __init__(self):
        # Load environment variables from .env file
        self._load_env_file()

        # Get API keys (try MY_API_KEY first, then fallback to standard names)
        self.anthropic_api_key = (
            os.getenv("MY_API_KEY") or
            os.getenv("ANTHROPIC_API_KEY")
        )
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Default generation settings
        self.model = "claude-sonnet-4-5-20250929"
        self.max_tokens = 20000  # Increased for thinking + output
        self.temperature = 0.7

        # Default evaluation criteria
        self.default_criteria = [
            "Impact on #1 product metric",
            "Confidence in impact",
            "Low implementation effort",
            "Level of innovation"
        ]

        # Output settings
        self.output_dir = "ideation_outputs"
        self.ensure_output_dir()

    def _load_env_file(self):
        """Load environment variables from .env file if it exists."""
        env_path = Path(__file__).parent / ".env"

        if not env_path.exists():
            return

        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Parse KEY=VALUE format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Set environment variable
                        os.environ[key] = value

        except Exception as e:
            # Silently fail if .env file can't be read
            pass

    def ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def has_api_key(self) -> bool:
        """Check if any API key is configured."""
        return bool(self.anthropic_api_key or self.openai_api_key)

    def get_api_key(self) -> Optional[str]:
        """Get the first available API key."""
        return self.anthropic_api_key or self.openai_api_key

    def get_model_provider(self) -> str:
        """Determine which model provider to use."""
        if self.anthropic_api_key:
            return "anthropic"
        elif self.openai_api_key:
            return "openai"
        else:
            return "none"
