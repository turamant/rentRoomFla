import os
from app import app
from app.models import Post, Tag, Category
#from flask_script import Manager, Shell
#from flask_migrate import MigrateCommand


if __name__ == '__main__':
    app.run(port=8000)