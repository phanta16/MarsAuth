from flask_restful import Resource, abort

import data.db_session
from data_api import *
from user_parser import parser


def abort_if_not_found(user_id):
    db_sess = data.db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found!")


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
            db_sess = data.db_session.create_session()
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
            db_sess.add(user)
            db_sess.commit()
            return jsonify({'success': 200})
        except Exception as e:
            return jsonify({'Something went wrong!': 404, 'message': str(e)})


class UserAPI(Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        db_sess = data.db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify(
            {
                'users': users.to_dict()
            }
        )

    def patch(self, user_id):
        abort_if_not_found(user_id)
        try:
            args = parser.parse_args()
            db_sess = data.db_session.create_session()
            users = db_sess.query(User).get(user_id)
            if 'name' in args and args['name'] is not None:
                users.name = args['name']

            if 'surname' in args and args['surname'] is not None:
                users.surname = args['surname']

            if 'age' in args and args['age'] is not None:
                users.age = args['age']

            if 'position' in args and args['position'] is not None:
                users.position = args['position']

            if 'speciality' in args and args['speciality'] is not None:
                users.speciality = args['speciality']

            if 'address' in args and args['address'] is not None:
                users.address = args['address']

            if 'email' in args and args['email'] is not None:
                users.email = args['email']

            if 'hashed_password' in args and args['hashed_password'] is not None:
                users.hashed_password = args['hashed_password']

            if 'modified_date' in args and args['modified_date'] is not None:
                users.modified_date = args['modified_date']

            db_sess.commit()
            return jsonify({'success': 200})
        except Exception as e:
            return jsonify({'Something went wrong!': 404, 'message': str(e)})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        db_sess = data.db_session.create_session()
        users = db_sess.query(User).get(user_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 200})
