# deproject/plugins/__init__.py
from .cors_patch import patch_cors

patch_cors()  # Airflow 웹서버가 뜰 때 CORS 허용 적용
