import os
from datetime import timedelta

class BaseConfig:
    """Base configuration class with common settings."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = False
    TESTING = False
    
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/findbestproduct')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Parser settings
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 2

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    MONGO_URI = os.getenv('DEV_MONGO_URI', BaseConfig.MONGO_URI)

class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = os.getenv('TEST_MONGO_URI', 'mongodb://localhost:27017/test_db')

class ProductionConfig(BaseConfig):
    """Production configuration."""
    MONGO_URI = os.getenv('PROD_MONGO_URI', BaseConfig.MONGO_URI)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
