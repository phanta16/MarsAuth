import flask
import flask_login
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

import data.db_session
from data.__all_models import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

data.db_session.global_init('db/users.db')


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Каюта', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if flask.session.get('get_logged_in', False):
        return flask.redirect('/')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db_sess = data.db_session.create_session()
        email = login_form.email
        password = login_form.password
        if db_sess.query(User).filter(User.email == email.data, User.hashed_password == password.data).first():
            us = db_sess.query(User).filter(User.email == email.data, User.hashed_password == password.data).first()
            print(us)
            flask.session['get_logged_in'] = True
            flask.session['name'] = us.name
            flask.session['surname'] = us.surname
            return flask.redirect('/')
        else:
            return render_template('login.html', form=login_form, message='Неверные данные!',
                                   current_user=flask_login.current_user)
    return render_template('login.html', form=login_form,
                           current_user=flask_login.current_user)


@app.route('/register', methods=['GET', 'POST'])
def reg_page():
    if flask.session.get('get_logged_in', False):
        return flask.redirect('/')
    registration_form = RegisterForm()
    name = registration_form.name.data
    surname = registration_form.surname.data
    age = registration_form.age.data
    position = registration_form.position.data
    speciality = registration_form.speciality.data
    address = registration_form.address.data
    email = registration_form.email.data
    password = registration_form.password.data
    if registration_form.validate_on_submit():
        db_sess = data.db_session.create_session()
        if not age.isdigit():
            return render_template('register.html.html', form=registration_form, message='Неверные данные!',
                                   current_user=flask_login.current_user)
        if db_sess.query(User).filter(User.email == email).first():
            return render_template('register.html', form=registration_form, message='Вы уже зарегистрированы!',
                                   current_user=flask_login.current_user)
        db_sess.add(User(name=name, surname=surname, hashed_password=password, age=int(age), position=position,
                         speciality=speciality,
                         address=address, email=email))
        db_sess.commit()
        return flask.redirect('/login')
    return render_template('register.html', form=registration_form, current_user=flask_login.current_user)


@app.route('/redirect_to_login/', methods=['GET', 'POST'])
def redirect_login_page():
    return flask.redirect('/login')


@app.route('/redirect_to_register/', methods=['GET', 'POST'])
def redirect_register_page():
    return flask.redirect('/register')

@app.route('/logout/')
def log_out():
    flask.session['get_logged_in'] = False
    return flask.redirect('/register')


@app.route('/')
def main():
    if 'get_logged_in' in flask.session:
        return render_template('main.html', name=flask.session.get('name', None),
                               surname=flask.session.get('surname', None), )
    return flask.redirect('/register')


if __name__ == '__main__':
    app.run()
