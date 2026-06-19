from flask import Flask
import config
from .models.database import Database

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    Database.create_tables()


    from app.routes.admin_auth_route import auth_admin
    app.register_blueprint(auth_admin)

    from app.routes.admindashboardroute import admin_dashboardBP
    app.register_blueprint(admin_dashboardBP)

    from app.routes.notificationroute import notificationBP
    app.register_blueprint(notificationBP)



    from app.routes.auth_route import auth_user
    app.register_blueprint(auth_user)

    

    from app.routes.home_route import homeBP
    app.register_blueprint(homeBP)

    from app.routes.setting_routes import settingBP
    app.register_blueprint(settingBP)

    from app.routes.report_route import report
    app.register_blueprint(report)


    from app.routes.my_report_route import my_report
    app.register_blueprint(my_report)

    return app