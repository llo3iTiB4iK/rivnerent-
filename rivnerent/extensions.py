from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
import requests


class Base(DeclarativeBase):
    pass


class SheetDBApi:
    def __init__(self):
        self.endpoint = None
        self.api_key = None

    def init_app(self, app):
        self.endpoint = app.config['SHEETDB_URL']
        self.api_key = app.config['SHEETDB_API_KEY']

    def get_column_names(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f'{self.endpoint}/keys', headers=headers)
        return response.json()

    def post_data(self, data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.endpoint, headers=headers, json=data)
        response.raise_for_status()


bootstrap = Bootstrap5()
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
sheetdb = SheetDBApi()
