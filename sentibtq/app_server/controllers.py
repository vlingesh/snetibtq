__author__ = 'patley'

from flask import Flask
from flask_restful import Api

import resources.health

skelton_app = Flask("generatr")
skelton_api = Api(skelton_app)

##Map relevant resources to resource identifiers

skelton_api.add_resource(resources.health.Health, "/health")
#generatr_api.add_resource(resources.health.Health, "/v1/health")