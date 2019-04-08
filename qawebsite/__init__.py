from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# SQLite for development postgres for production
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)

from qawebsite import routes
