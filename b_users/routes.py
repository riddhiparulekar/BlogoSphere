from b_users import users_bp
from flask import render_template, request, redirect, url_for
from .models import User
from .forms import SigninForm, SignupForm, UserForm
from .utils import fetch_all_countries
from extension import database, bcrypt, login_man
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

@users_bp.route("/home")
@users_bp.route("/")
def home():
    return render_template('home.html')

@users_bp.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@users_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        encrypt_password = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name = form.first_name.data, last_name = form.last_name.data, email_id = form.email_id.data, password = encrypt_password, country=form.country.data)
        database.session.add(user)
        database.session.commit()
        return redirect(url_for('users.signin'))
    return render_template('signup.html', form=form)


@users_bp.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_id=form.email_id.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.home'))
    return render_template('login.html', form=form)


@users_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('users.signin'))

@login_man.user_loader
def userload(id):
    return User.query.get(int(id))


@users_bp.route("/profile", methods=['GET', 'POST'])
def profile():
    user = User.query.get(current_user.id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        database.session.commit()
    return render_template('profile.html', form=form)