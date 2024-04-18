from flask import Flask, url_for
from blogs import blogs_bp
from b_users import users_bp
from extension import database, bcrypt, login_man


#intance variable created and run
app = Flask(__name__) # dynamic name of class / file /name->__name__
app.register_blueprint(blogs_bp)
app.register_blueprint(users_bp)


#Env variables 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'temp_key'


#initialise database 
database.init_app(app)
bcrypt.init_app(app)
login_man.init_app(app)
login_man.login_view = 'users.signin'


with app.app_context():
    database.create_all()


if __name__ == "__main__":
    app.run(debug=True)