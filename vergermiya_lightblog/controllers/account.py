from os import path
from uuid import uuid4

from flask import flash, url_for, redirect, render_template, Blueprint

from vergermiya_lightblog.forms import LoginForm, RegisterForm
from vergermiya_lightblog.models import db, User


account_blueprint = Blueprint("account", __name__,
                              template_folder=path.join(path.pardir, "templates", "account"))


@account_blueprint.route('/')
def index():
    return redirect(url_for('blog.index'))


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.index'))

    return render_template('login.html', form=form)


@account_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("You have been logged out.", category="success")

    return redirect(url_for('blog.index'))


@account_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please login.', category="success")
        return  redirect(url_for('account.login'))

    return render_template('register.html', form=form)
