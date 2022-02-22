import email
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user

from ..models import Staff
from .forms import LoginForm


staff = Blueprint('staff', __name__)

@staff.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        staff = Staff.query.filter_by(email=email).first()

        if staff is None or not staff.check_password(password):
            flash('ログイン情報をご確認下さい。')
            return redirect(url_for('staff.login'))

        login_user(staff, remember=True)
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)


@staff.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('staff.login'))