# deproject/plugins/cors_patch.py
from flask_cors import CORS
from airflow.www.app import cached_app

def patch_cors():
    app = cached_app()
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})