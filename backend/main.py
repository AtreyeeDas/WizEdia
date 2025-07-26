#!/usr/bin/env python3
"""
WizEdia Flask Backend - Main Application Entry Point
A Hogwarts-inspired intelligent learning companion backend
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import blueprints
from api.pensieve import pensieve_bp
from api.riddlenet import riddlenet_bp
from api.hermione_chat import hermione_bp
from api.potion_mixer import potion_bp
from api.erised_quotes import erised_bp
from api.prophecy_engine import prophecy_bp
from api.marauder_map import marauder_bp
from api.forbidden_library import library_bp
from api.professor_pods import pods_bp

# Import config
from config.firebase_config import initialize_firebase

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for all domains and all routes
    CORS(app, origins=["http://localhost:5173"], allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])
    
    # Initialize Firebase
    initialize_firebase()
    
    # Register blueprints
    app.register_blueprint(pensieve_bp, url_prefix='/api/pensieve')
    app.register_blueprint(riddlenet_bp, url_prefix='/api/riddlenet')
    app.register_blueprint(hermione_bp, url_prefix='/api/hermione')
    app.register_blueprint(potion_bp, url_prefix='/api/potion')
    app.register_blueprint(erised_bp, url_prefix='/api/erised')
    app.register_blueprint(prophecy_bp, url_prefix='/api/prophecy')
    app.register_blueprint(marauder_bp, url_prefix='/api/marauder')
    app.register_blueprint(library_bp, url_prefix='/api/library')
    app.register_blueprint(pods_bp, url_prefix='/api/pods')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'WizEdia Backend is running successfully! 🧙‍♂️',
            'version': '1.0.0'
        })
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to WizEdia - Your Hogwarts Learning Companion! 🏰',
            'endpoints': {
                'pensieve': '/api/pensieve/analyze',
                'riddlenet': '/api/riddlenet/respond',
                'hermione': '/api/hermione/chat',
                'potion': '/api/potion/mix',
                'erised': '/api/erised/quote',
                'prophecy': '/api/prophecy/calendar-alerts',
                'marauder': '/api/marauder/events',
                'library': '/api/library/summarize',
                'pods': '/api/pods/recommend'
            }
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found in the magical realm'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'A magical mishap occurred on our end'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])