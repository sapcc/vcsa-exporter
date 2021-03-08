from flask.views import MethodView
from flask import request
import json


class RequestHandler(MethodView):
    def __init__(self):
        with open('../mockingServer/data/login.json', 'r') as data:
            self.session_id = json.load(data)

    def check_session_id(self):
        if request.headers.environ['HTTP_VMWARE_API_SESSION_ID'] != self.session_id['value']:
            return False
        return True
