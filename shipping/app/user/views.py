from crypt import methods
import email
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user

from ..models import SupplierUser
from .forms import LoginForm

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.index'))

    form = LoginForm()

    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        user = SupplierUser.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('メールアドレス/パスワードを確認してください。')
            return redirect(url_for('user.login'))

        login_user(user, remember=True)
        return redirect(url_for('view.index'))

    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('user.login'))
