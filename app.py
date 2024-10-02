from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()

# Определение функции user_loader
from models import User
# @login_manager.user_loader

# def load_user(user_id):
#     return User.query.get(int(user_id))  # Возвращаем пользователя по его идентификатору

def create_app():
    app = Flask(__name__, template_folder='templates')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)
    migrate = Migrate(app, db)

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # bcrypt = Bcrypt(app)

    login_manager.login_view = 'login'  # Устанавливаем страницу для входа
    login_manager.login_message = "Please log in to access this page."  # Сообщение при редиректе

    # Импортируем маршруты из routes.py
    from routes import init_routes
    init_routes(app, db)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    # from auth import auth_routes
    # auth_routes(app, db, bcrypt)

    return app

