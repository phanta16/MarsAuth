import datetime

from flask_restful import Api
import flask_login
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

import data.db_session
import user_resources
from data.__all_models import User, Jobs
from data_api import *
import data_api

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

data.db_session.global_init('db/users.db')

# app.register_blueprint(data_api.blueprint)
api.add_resource(user_resources.UsersAPI, '/api/users')
api.add_resource(user_resources.UserAPI, '/api/users/<int:user_id>')


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


class JobForm(FlaskForm):
    job = StringField('Наименование деятельности', validators=[DataRequired()])
    collaborators = StringField('Помощники', validators=[DataRequired()])
    work_size = StringField('Размер проделанной работы', validators=[DataRequired()])
    date_of_end = StringField('Через сколько дней будет окончена работа', validators=[DataRequired()])
    submit = SubmitField('Занести в Базу Данных')


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
            flask.session['get_logged_in'] = True
            flask.session['id'] = us.id
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


@app.route('/make_new_post/', methods=['GET', 'POST'])
def make_new_post():
    db_sess = data.db_session.create_session()
    job_form = JobForm()
    if not flask.session.get('get_logged_in', False):
        return flask.redirect('/')
    else:
        if job_form.validate_on_submit():
            job_name = job_form.job.data
            job_size = job_form.work_size.data
            job_collab = job_form.collaborators.data
            team_leader = flask.session.get('id', None)
            db_sess.add(Jobs(job=job_name, team_leader=team_leader, work_size=int(job_size), collaborators=job_collab,
                             start_date=datetime.datetime.now(),
                             end_date=datetime.datetime.now() + datetime.timedelta(
                                 days=int(job_form.date_of_end.data)), is_finished=False))
            db_sess.commit()
            return flask.redirect('/')
    return render_template('jobs.html', form=job_form, current_user=flask_login.current_user)


@app.route('/')
def main():
    db_sess = data.db_session.create_session()
    cur_user = db_sess.query(User).filter(User.id == flask.session.get('id', None)).first()
    if 'get_logged_in' in flask.session:
        return render_template('main.html', name=cur_user.name,
                               surname=cur_user.name)
    return flask.redirect('/register')






if __name__ == '__main__':
    app.run()
