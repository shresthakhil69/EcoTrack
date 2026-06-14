from flask import Flask
import config
from .models.database import Database

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    Database.create_tables()

    from app.routes.auth_for_admin import auth_admin
    app.register_blueprint(auth_admin)

    from app.routes.admindashboardroute import admin_dashboardBP
    app.register_blueprint(admin_dashboardBP)




    

    from app.routes.auth_for_user import auth_user
    app.register_blueprint(auth_user)

    from app.routes.dashboardroute import dashboardBP
    app.register_blueprint(dashboardBP)

    from app.routes.homeroute import homeBP
    app.register_blueprint(homeBP)

    from app.routes.my_reportroute import my_reportBP
    app.register_blueprint(my_reportBP)

    from app.routes.notificationroute import notificationBP
    app.register_blueprint(notificationBP)

    from app.routes.report_successroute import report_successBP
    app.register_blueprint(report_successBP)

    from app.routes.reportsroute import reportsBP
    app.register_blueprint(reportsBP)

    from app.routes.settingroute import settingBP
    app.register_blueprint(settingBP)

    return app
