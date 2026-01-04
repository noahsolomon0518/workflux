"""
Configuration file for Stock Size Selector
Copy this to config.py and update with your settings
"""

class Config:
    # Flask settings
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True
    
    # Database settings (for future implementation)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///stock_selector.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/stock_selector'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Material Provider API Keys (for future implementation)
    # MCMASTER_API_KEY = 'your-api-key'
    # ONLINEMETALS_API_KEY = 'your-api-key'
    # METALSDEPOT_API_KEY = 'your-api-key'
    
    # Optimization settings
    STOCK_SIZE_TOLERANCE = 0.125  # inches
    DEFAULT_MATERIAL_MARKUP = 1.15  # 15% markup
    
    # Price caching (for future Redis implementation)
    # REDIS_URL = 'redis://localhost:6379/0'
    # CACHE_TIMEOUT = 3600  # 1 hour
    
    # Email settings (for alerts - future)
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'your-email@example.com'
    # MAIL_PASSWORD = 'your-password'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add production-specific settings

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
