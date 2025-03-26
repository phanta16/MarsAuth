from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('team_leader')
parser.add_argument('job')
parser.add_argument('work_size')
parser.add_argument('collaborators')
parser.add_argument('is_finished')
parser.add_argument('hashed_password')
parser.add_argument('start_date')
parser.add_argument('end_date')