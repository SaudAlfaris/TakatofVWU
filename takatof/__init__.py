from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from takatof.config import SECRET_KEY, DB_URI
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_view = "login"
login_manager.login_message = "يجب تسجيل الدخول لإستخدام هذه الصفحة."

from takatof import routes
