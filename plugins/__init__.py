# deproject/plugins/__init__.py
from flask import Flask
from .cors_middleware import apply_cors_middleware

def patch_flask_app():
    from airflow.www.app import cached_app
    app = cached_app()
    apply_cors_middleware(app)

patch_flask_app()
