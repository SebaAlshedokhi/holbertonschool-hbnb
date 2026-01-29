#!/usr/bin/env python3
"""
Run script for the HBnB application.
"""
import os
from hbnb.app import create_app

# Get configuration from environment variable or use default
config_name = os.getenv('FLASK_ENV', 'development')
config_class = f'config.{config_name.capitalize()}Config' if config_name != 'development' else 'config.DevelopmentConfig'

app = create_app(config_class)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=app.config.get('DEBUG', False)
    )
