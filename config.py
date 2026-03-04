"""
Configuration management for Project Lazarus Gate.
Centralized configuration with validation and type safety.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str
    private_key: str
    client_email: str
    
    def __post_init__(self):
        """Validate Firebase configuration"""
        if not all([self.project_id, self.private_key, self.client_email]):
            raise ValueError("All Firebase configuration values must be provided")
        # Clean private key format for Firebase Admin
        if "\\n" in self.private_key:
            self.private_key = self.private_key.replace("\\n", "\n")

@dataclass
class AIConfig:
    """AI model configuration"""
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    def __post_init__(self):
        """Validate AI configuration"""
        if not self.api_key:
            raise ValueError("API key is required")
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")

@dataclass
class SystemConfig:
    """System operation configuration"""
    max_retries: int = 3
    retry_delay: int = 5
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Validate system configuration"""
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")
        if self.retry_delay < 0:
            raise ValueError("Retry delay cannot be negative")
        
        # Set up logging
        numeric_level = getattr(logging, self.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {self.log_level}")
        
        logging.b