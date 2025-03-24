from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('age')
parser.add_argument('position')
parser.add_argument('speciality')
parser.add_argument('address')
parser.add_argument('email')
parser.add_argument('hashed_password')
parser.add_argument('modified_date')