"""Configuration management for Peter Tweets."""

import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Configuration following Peter's patterns - environment-based, simple."""
    
    def __init__(self):
        # Load .env from various locations
        load_dotenv(Path.home() / "clawd" / ".env")
        load_dotenv()
        
        self.base_dir = Path.home() / "clawd" / "peter-tweets"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Core settings
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET", "")
        
        # Target user
        self.target_user = "steipete"
        self.target_user_id = None  # Will be fetched on first run
        
        # Parallel agent settings
        self.num_agents = 5
        self.poll_interval_minutes = 15
        self.wisdom_threshold = 7
        
        # Paths
        self.db_path = self.base_dir / "data" / "tweets.db"
        self.log_dir = self.base_dir / "logs"
        self.export_dir = self.base_dir / "exports"
        
        # Create directories
        for dir_path in [self.db_path.parent, self.log_dir, self.export_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Rate limiting
        self.rate_limit_calls = 900  # Per 15 min window
        self.rate_limit_window = 900  # 15 minutes
        
        # Self-healing
        self.max_retries = 3
        self.retry_delay = 5
        self.health_check_interval = 300  # 5 minutes
        
        # Load any saved config
        self._load_saved_config()
        
    def _load_saved_config(self):
        """Load saved configuration if exists."""
        config_file = self.base_dir / "config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                saved_config = json.load(f)
                
            # Override with saved values
            for key, value in saved_config.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
    def save(self):
        """Save current configuration."""
        config_file = self.base_dir / "config.json"
        
        config_dict = {
            "target_user": self.target_user,
            "target_user_id": self.target_user_id,
            "num_agents": self.num_agents,
            "poll_interval_minutes": self.poll_interval_minutes,
            "wisdom_threshold": self.wisdom_threshold,
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)
            
    def validate(self) -> Dict[str, Any]:
        """Validate configuration is ready."""
        issues = []
        
        if not self.twitter_bearer_token and not (self.twitter_api_key and self.twitter_api_secret):
            issues.append("Missing Twitter API credentials")
            
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }