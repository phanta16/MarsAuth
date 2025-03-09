import flask
import flask_login
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import data.db_session
from data import *
from data.__all_models import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

data.db_session.global_init('db/users.db')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'get_logged_in' in flask.session:
        return flask.redirect('/')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db_sess = db_session.create_session()
        email = login_form.email
        password = login_form.password
        if not db_sess.query(User).filter(User.email == email.data, User.hashed_password == password.data).first():
            db_sess.add(User(email=email.data, hashed_password=password.data))
            db_sess.commit()
            get_logged_in = flask.session.get('get_logged_in', 0)
            flask.session['get_logged_in'] = get_logged_in + 1
            return flask.redirect('/')
        else:
            if password.data in db_sess.query(User).filter(User.email == email.data, User.hashed_password == password.data).first() and email.data in db_sess.query(
                User).filter_by(User.email == email.data, User.hashed_password == password.data).first():
                get_logged_in = flask.session.get('get_logged_in', 0)
                flask.session['get_logged_in'] = get_logged_in + 1
                return flask.redirect('/')
            else:
                return render_template('login.html', form=login_form, message='Неверный пароль!',
                                       current_user=flask_login.current_user)
    return render_template('login.html', form=login_form, current_user=flask_login.current_user)


@app.route('/')
def main():
    if 'get_logged_in' in flask.session:
        print(1)
        return render_template('main.html')
    return flask.redirect('/login')


if __name__ == '__main__':
    app.run()
