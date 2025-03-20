from flask import Blueprint
import data.db_session
import data_api
from data.__all_models import Jobs
from data_api import *
from flask import jsonify
import flask

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
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'start_date', 'end_date', 'is_finished')) for item in jobs
                 ]
        }
    )