from flask import Flask
import config
from .models.database import Database

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    Database.create_tables()

    from app.routes.admin_auth_route import auth_admin
    app.register_blueprint(auth_admin)
    

    from app.routes.auth_route import auth_user
    app.register_blueprint(auth_user)

    from app.routes.home_route import homeBP
    app.register_blueprint(homeBP)

    from app.routes.setting_routes import settingBP
    app.register_blueprint(settingBP)


    return app
