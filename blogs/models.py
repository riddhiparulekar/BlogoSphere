from flask_login import UserMixin
from extension import database
from datetime import datetime
from sqlalchemy import Enum
import enum


class Category(enum.Enum):
    lifestyle = 'Lifestyle'
    technology = 'Technology'
    education_career = 'Education and Career'


class Blogs(database.Model, UserMixin):
    __tablename__ = 'blogs'
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(150), nullable = False)
    blog_content = database.Column(database.Text, nullable = False)
    
    author_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    author = database.relationship("User", backref=database.backref("blogs", uselist = False))

    no_of_views = database.Column(database.Integer, nullable = False, default=0)
    category = database.Column(Enum(Category), nullable=False)
    publish_datetime= database.Column(database.DateTime, default = datetime.utcnow)
    
    blog_image = database.Column(database.Text, nullable = False)
    blog_image_name = database.Column(database.String(50), nullable = False)
    blog_image_mimetype = database.Column(database.Text, nullable = False)


class Comments(database.Model, UserMixin):
    __tablename__ = "comments"
    id = database.Column(database.Integer, primary_key = True)
    comment = database.Column(database.String(1000), nullable = False)
    blog_id = database.Column(database.Integer, database.ForeignKey('blogs.id'))
    blog = database.relationship("Blogs", backref=database.backref("comments", uselist = False))

    author_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    author = database.relationship("User", backref=database.backref("comments", uselist = False))

    publish_datetime= database.Column(database.DateTime, default = datetime.utcnow)

    neg_sentiment_score = database.Column(database.Numeric(3,2))
    neu_sentiment_score = database.Column(database.Numeric(3,2))
    pos_sentiment_score = database.Column(database.Numeric(3,2))
    compound_sentiment_score = database.Column(database.Numeric(3,2))



