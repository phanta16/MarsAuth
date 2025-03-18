from flask import Blueprint
import data.db_session
from data.__all_models import User


blueprint = Blueprint('jobs', __name__)

@app.blueprint.route('/jobs/api', methods=['GET'])
def get_jobs():
    pass
