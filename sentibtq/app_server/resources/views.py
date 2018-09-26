__author__ = 'patley'

from flask import jsonify
from jinja2 import Environment, FileSystemLoader
from werkzeug import Response
import os


def __get_response(**kwargs):
    return jsonify(**kwargs)


def get_success_response(**kwargs):
    new_resp = dict(stat="ok", data=kwargs)
    return __get_response(**new_resp)


def get_fail_response(**kwargs):
    new_resp = dict(stat="fail", data=kwargs)
    return __get_response(**new_resp)


def web_response(html_template, template_args):
    jinja_env = Environment(loader=FileSystemLoader(os.getcwd()+"/templates"),
                         trim_blocks=True)
    template = jinja_env.get_template(html_template)
    return Response(response=template.render(**template_args),
                        content_type="text/html",
                        status=200)
