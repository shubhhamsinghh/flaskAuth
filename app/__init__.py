from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os
from .extensions import mail

#create DB object globally
db = SQLAlchemy() # database object
migrate = Migrate() # migration engine


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-development-secret-key'
    app.config['ENV'] = 'development' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskAuth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'profile')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'shubhamproject09882@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vxfx tdaz uhbh bsbb'

    db.init_app(app)  # connect DB to app
    migrate.init_app(app, db)  # connect Migrate to app and DB
    csrf = CSRFProtect(app)
    mail.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.users import users_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)

    from app.models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('auth.login'))

    @app.context_processor
    def current_year():
        return {'current_year': datetime.now().year}

    return app

