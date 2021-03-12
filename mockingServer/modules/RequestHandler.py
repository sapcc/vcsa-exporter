from flask.views import MethodView
from flask import request
import json


class RequestHandler(MethodView):
    def __init__(self):
        self.session_id = {'value': '779b8ede-1337-11eb-9581-3c58c27e75a6'}

    def check_session_id(self):
        if request.headers.environ['HTTP_VMWARE_API_SESSION_ID'] != self.session_id['value']:
            return False
        return True
