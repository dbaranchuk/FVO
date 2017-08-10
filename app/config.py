CSRF_ENABLED = True
SECRET_KEY = 'super-SecreT-fVO-MSU-KeY'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
USER_PATH = os.path.join(basedir, 'static', 'user_data')
SQLALCHEMY_TRACK_MODIFICATIONS = False