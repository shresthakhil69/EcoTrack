from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

from app.routes.report_route import report
from app.routes.my_report_route import my_report

app.register_blueprint(report)
app.register_blueprint(my_report)