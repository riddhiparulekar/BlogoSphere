from flask_sqlalchemy import SQLAlchemy #Database forORM
from flask_bcrypt import Bcrypt #Password Encryption
from flask_login import LoginManager #Flask Authentications


database= SQLAlchemy()
bcrypt =Bcrypt()
login_man =LoginManager()

 