from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.log_in'

    from app.blueprints.auth import auth_bp
    from app.blueprints.tasks import tasks_bp
    from app.blueprints.admin import admin_bp  
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(admin_bp)  

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
