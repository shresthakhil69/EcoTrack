from flask import Flask
import config
from .models.database import Database
from flask_login import LoginManager
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    Database.create_tables()

    def strftime_filter(value, format):
        if value is None:
            return ""
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value.strftime(format)

    app.jinja_env.filters['strftime'] = strftime_filter

    # Register Admin Auth Blueprint
    from app.routes.admin_auth_route import auth_admin
    app.register_blueprint(auth_admin)

    from app.routes.admindashboardroute import admin_dashboardBP
    app.register_blueprint(admin_dashboardBP)

    from app.routes.notificationroute import notificationBP
    app.register_blueprint(notificationBP)


    # Register User Auth Blueprint
    from app.routes.auth_route import auth_user
    app.register_blueprint(auth_user)

    # Register Home Blueprint
    from app.routes.home_route import homeBP
    app.register_blueprint(homeBP)

    # Register Setting Blueprint
    from app.routes.setting_routes import settingBP
    app.register_blueprint(settingBP)

    # Register Report Blueprint
    from app.routes.report_route import report
    app.register_blueprint(report)

    # Register My Report Blueprint (FIXED NAME HERE)
    from app.routes.my_report_route import my_report
    app.register_blueprint(my_report)

    return app