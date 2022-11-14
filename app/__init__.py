import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '813325e329ada54fd27a3c1248a14529'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '167a3314ccf0d5'
app.config['MAIL_PASSWORD'] = '390e5509cae7a6'
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'johngrant685@gmail.com'
# app.config['MAIL_PASSWORD'] = 'bmnuwpwykxoytdwv'
# app.config['MAIL_DEFAULT_SENDER'] = 'noreply@gmail.com'
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_MAX_EMAILS'] = None
mail = Mail(app)


from app import routes
