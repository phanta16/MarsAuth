from flask_restful import Resource, abort, reqparse

import data.db_session
from data_api import *
from user_parser import parser

def abort_if_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersAPI(Resource):
    def get(self):
        db_sess = data.db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict() for
                     item in users
                     ]
            }
        )

    def post(self):
        try:
            args = parser.parse_args()
            session = db_session.create_session()
            user = User(
                email=args['email'],
                hashed_password=args['hashed_password'],
                modified_date=args['modified_date'],
                surname=args['surname'],
                name=args['name'],
                age=args['age'],
                position=args['position'],
                speciality=args['speciality'],
                address=args['address'],

            )
            session.add(user)
            session.commit()
            return jsonify({'success': 200})
        except Exception as e:
            return jsonify({'Something went wrong!': 404, 'message': str(e)})


class UserAPI(Resource):
    def get(self, uid):
        abort_if_not_found(uid)
        db_sess = data.db_session.create_session()
        users = db_sess.query(User).get(uid)
        if not users:
            return flask.make_response(jsonify({'error': 'Не найдено!'}), 404)
        return jsonify(
            {
                'users': users.to_dict()
            }
        )

    def patch(self, uid):
        abort_if_not_found(uid)
        pass

    def delete(self, uid):
        abort_if_not_found(uid)
        pass
