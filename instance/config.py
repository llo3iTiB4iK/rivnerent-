import os

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = 'sqlite:///cars.db'
ADMIN_PHONE = os.environ.get("ADMIN_PHONE")
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
SHEETDB_URL = os.environ.get("SHEETDB_URL")
SHEETDB_API_KEY = os.environ.get("SHEETDB_API_KEY")
