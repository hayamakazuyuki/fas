from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required,logout_user

from ..models import CustomerUser
from .forms import LoginForm

user = Blueprint('user',__name__)

@user.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cs.index'))

    form = LoginForm()
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('user.login'))
