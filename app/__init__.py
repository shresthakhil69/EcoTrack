from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

from app.routes.report_route import report

app.register_blueprint(report)