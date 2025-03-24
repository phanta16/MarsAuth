import flask
from flask import jsonify
from flask import request

from flask import Blueprint
import datetime
import data.db_session
from data.__all_models import User, Jobs
from data_api import *
from flask import make_response
blueprint = Blueprint('jobs', __name__)


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = data.db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.make_response(jsonify({'error': 'Не найдено!'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs/', methods=['GET'])
def get_jobs():
    db_sess = data.db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished')) for
                 item in jobs
                 ]
        }
    )


@blueprint.route('/api/jobs/', methods=['POST'])
def add_jobs():
    db_sess = data.db_session.create_session()
    dataa = request.get_json()
    try:
        db_sess.add(Jobs(job=dataa['name'], team_leader=dataa['team_leader_id'], work_size=int(dataa['work_size']),
                         collaborators=dataa['job_collab'],
                         start_date=datetime.datetime.now(),
                         end_date=datetime.datetime.now() + datetime.timedelta(
                             days=int(dataa['finish'])), is_finished=False))
        db_sess.commit()
        return jsonify({'success': 200})
    except Exception as e:
        return flask.make_response(jsonify({'error': 'Incorrect data!'}), 404)


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def del_jobs(jobs_id):
    db_sess = data.db_session.create_session()
    try:
        db_sess.delete(db_sess.query(Jobs).get(jobs_id))
        db_sess.commit()
        return  jsonify({'success': 200})
    except Exception as e:
        return flask.make_response(jsonify({'error': 'Incorrect data!'}), 404)


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PATCH'])
def patch_jobs(jobs_id):
    db_sess = data.db_session.create_session()
    dataa = request.get_json()
    jobs = db_sess.query(Jobs).get(jobs_id)
    try:
        if 'name' in dataa:
            jobs.job = dataa['name']
        if 'work_size' in dataa:
            jobs.work_size = dataa['work_size']
        if 'collaborators' in dataa:
            jobs.collaborators = dataa['collaborators']
        if 'finish' in dataa:
            jobs.is_finished = dataa['finish']
        db_sess.commit()
        return jsonify({'success': 200})
    except Exception as e:
        return flask.make_response(jsonify({'error': 'Incorrect data!'}), 404)
