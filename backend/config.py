import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Data paths
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
    LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
    CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
    
    # Create directories if they don't exist
    for directory in [DATA_DIR, LOG_DIR, CACHE_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Versioning
    CURRENT_VERSION = "1.0.0"
    PIPELINE_VERSION = "2026-06-08-v1"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    return config.get(env, config['default'])
