import util,sqlconn
import string
_file = util.readpass

class ConfigClass(object):
    import os
    # Flask settings
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'this is a secret key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'mysql://'+_file['mysqluser']+
                                        ':'+_file['mysqlpasswd']+'@'+_file['hostname']+'/'+
                                        _file['database'])
    #mysql://username:password@server/db
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        _file['email'])
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        _file['emailpass'])
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  _file['email'])
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          string.split(_file['emailsmtp'],':')[0])
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            string.split(_file['emailsmtp'],':')[1]))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "S.Yang"                # Used by email templates
    SQLALCHEMY_POOL_RECYCLE = 300
######################################################################

import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask import Flask
import flask_compress as Compress

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

from intro_to_flask.routes import mail
mail.init_app(app)

    # Initialize Flask extensions
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
mail = Mail(app)                                # Initialize Flask-Mail

from intro_to_flask.models import db, User2, User

    # Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
