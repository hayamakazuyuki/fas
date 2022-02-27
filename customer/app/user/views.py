from crypt import methods
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required,logout_user,login_user

from ..models import CustomerUser
from .forms import LoginForm

user = Blueprint('user',__name__)

@user.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('cs.index'))

    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        user = CustomerUser.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('ログイン情報をご確認ください。')
            return redirect(url_for('user.login'))

        login_user(user, remember=True)

        return  redirect(url_for('cs.index'))

    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('user.login'))
