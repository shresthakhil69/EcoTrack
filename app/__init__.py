from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return None

from app.routes.home_route import home
from app.routes.auth_route import auth
from app.routes.my_report_route import my_report
from app.routes.report_route import report

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(my_report)
app.register_blueprint(report)




