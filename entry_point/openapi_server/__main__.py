#!/usr/bin/env python3

import connexion

from openapi_server import encoder

def create_app():
    connexion_app = connexion.App(__name__, specification_dir='./openapi/')
    
    connexion_app.app.json_encoder = encoder.JSONEncoder
    connexion_app.add_api('openapi.yaml',
                arguments={'title': 'API Contract between client and entry point'},
                pythonic_params=True)
    
    flask_app = connexion_app.app  # Get Flask app with routes already registered
    return flask_app

def main():
    """For development server only."""
    app = create_app()
    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
