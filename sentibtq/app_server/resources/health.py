__author__ = 'patley'

import app_server.views as views
from flask_restful import Resource


class Health(Resource):
    def get(self):
        return views.get_success_response(**{"ping": "pong"})
