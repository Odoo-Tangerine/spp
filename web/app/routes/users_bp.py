import asyncio
from functools import wraps
from flask import Blueprint, render_template, redirect, session, current_app, flash, url_for
from flask_wtf import FlaskForm
from flask_caching import Cache
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

from ..common.messages import Categories, UserMessage
from ..common.odoo_api import UserAPI

users = Blueprint('users', __name__, url_prefix='/users')
cache = Cache(current_app)


class MainUserForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField(validators=[InputRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField()


class SignInForm(MainUserForm):
    remember_me = BooleanField()


class SignUpForm(MainUserForm):
    fullname = StringField(validators=[InputRequired()], render_kw={'placeholder': 'Full name'})
    phone = StringField(validators=[InputRequired()], render_kw={'placeholder': 'Phone number'})
    confirm_password = PasswordField(validators=[InputRequired(),
                                                 EqualTo('password')], render_kw={'placeholder': 'Confirm password'})


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('user') and '__uid' in session.get('user'):
            return f(*args, **kwargs)
        else:
            flash(UserMessage.LoginRequired.value, Categories.Error.value)
            return redirect('/')

    return wrap


@users.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    sign_in_form = SignInForm()
    if sign_in_form.validate_on_submit():
        email = sign_in_form.email.data
        password = sign_in_form.password.data
        if not email:
            flash(UserMessage.EmailRequired.value, Categories.Error.value)
        elif not password:
            flash(UserMessage.PasswordRequired.value, Categories.Error.value)
        response = asyncio.run(UserAPI.sign_in(email, password))
        if not response:
            flash(UserMessage.LoginFailed.value, Categories.Error.value)
            return redirect(url_for('users.sign_in'))
        else:
            session['user'] = dict(__uid=response['uid'], __name=response['name'], __username=response['username'])
            flash(UserMessage.LoginSuccess.value, Categories.Success.value)
            return redirect('/')
    elif session.get('users'):
        return redirect('/users/profile')
    return render_template('/users/sign_in.html', sign_in_form=sign_in_form)


@users.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        email = sign_up_form.email.data
        password = sign_up_form.password.data
        fullname = sign_up_form.fullname.data
        if not email:
            flash(UserMessage.EmailRequired.value, Categories.Error.value)
        elif not password:
            flash(UserMessage.PasswordRequired.value, Categories.Error.value)
        elif not fullname:
            flash(UserMessage.FullnameRequired.value, Categories.Error.value)
        response = asyncio.run(UserAPI.sign_up(email, password, fullname))
        return redirect('/users/sign_in')
    return render_template('/users/sign_up.html', sign_up_form=sign_up_form)


@users.route('/forgot_password')
def forgot_password():
    return render_template('/users/forgot_password.html')


@users.route('/sign_out')
@login_required
def sign_out():
    response = asyncio.run(UserAPI.sign_out())
    session.pop('user', None)
    return redirect('/')


@users.route('/profile', methods=['GET'])
@login_required
def profile():
    profile = asyncio.run(UserAPI.profile(session['user']['__uid']))
    return render_template('/users/profile.html', profile=profile)
