from flask_login import UserMixin
from extension import database


class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key = True)
    first_name = database.Column(database.String(30), nullable = False)
    last_name = database.Column(database.String(50), nullable = False)
    email_id = database.Column(database.String(30),nullable = False, unique = True)
    password = database.Column(database.String(30), nullable = False)
    country = database.Column(database.String(50), nullable=True)

