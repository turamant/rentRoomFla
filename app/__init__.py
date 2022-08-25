from flask import Flask
#from flask_migrate import Migrate, MigrateCommand
#from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager, Command, Shell
#from flask_login import LoginManager
import os, config

# создание экземпляра приложения
app = Flask(__name__, template_folder="jinja_templates",  static_folder="static_dir")
app.config.from_object('config.DevelopementConfig')

# инициализирует расширения
db = SQLAlchemy(app)
#mail = Mail(app)
#migrate = Migrate(app, db)
#login_manager = LoginManager(app)
#login_manager.login_view = 'login'

#import views
from . import views
# from . import forum_views
# from . import admin_views