from flask_restful import Resource, abort

import data.db_session
from data_api import *
from jobs_parser import parser


def abort_if_not_found(jobs_id):
    db_sess = data.db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Job {jobs_id} not found!")


class JobsAPI(Resource):
    def get(self):
        db_sess = data.db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict() for
                     item in jobs
                     ]
            }
        )

    def post(self):
        try:
            args = parser.parse_args()
            db_sess = data.db_session.create_session()
            job = Jobs(
                team_leader=args['team_leader'],
                job=args['job'],
                work_size=args['work_size'],
                start_date=args['start_date'],
                end_date=args['end_date'],
                collaborators=args['collaborators'],
                is_finished=args['is_finished'],

            )
            db_sess.add(job)
            db_sess.commit()
            return jsonify({'success': 200})
        except Exception as e:
            return jsonify({'Something went wrong!': 404, 'message': str(e)})


class JobAPI(Resource):
    def get(self, jobs_id):
        abort_if_not_found(jobs_id)
        db_sess = data.db_session.create_session()
        users = db_sess.query(Jobs).get(jobs_id)
        return jsonify(
            {
                'jobs': users.to_dict()
            }
        )

    def patch(self, jobs_id):
        abort_if_not_found(jobs_id)
        try:
            args = parser.parse_args()
            db_sess = data.db_session.create_session()
            jobs = db_sess.query(Jobs).get(jobs_id)
            if 'team_leader' in args and args['team_leader'] is not None:
                jobs.team_leader = args['team_leader']

            if 'job' in args and args['job'] is not None:
                jobs.job = args['job']

            if 'work_size' in args and args['work_size'] is not None:
                jobs.work_size = args['work_size']

            if 'collaborators' in args and args['collaborators'] is not None:
                jobs.collaborators = args['collaborators']

            if 'start_date' in args and args['start_date'] is not None:
                jobs.start_date = args['start_date']

            if 'end_date' in args and args['end_date'] is not None:
                jobs.end_date = args['end_date']

            if 'is_finished' in args and args['is_finished'] is not None:
                jobs.is_finished = args['is_finished']
            db_sess.commit()
            return jsonify({'success': 200})
        except Exception as e:
            return jsonify({'Something went wrong!': 404, 'message': str(e)})

    def delete(self, jobs_id):
        abort_if_not_found(jobs_id)
        db_sess = data.db_session.create_session()
        job = db_sess.query(Jobs).get(jobs_id)
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'success': 200})
