from mockingServer.modules.RequestHandler import RequestHandler
from flask import Blueprint, make_response
import json

loggingBluePrint = Blueprint('LoggingService', import_name=__name__)


class LoggingService(RequestHandler):
    def post(self):
        if not self.check_session_id():
            return make_response('sessionID check failed', 401)
        with open('mockingServer/data/logging.json', 'r') as data:
            response = json.load(data)
        return response


loggingBluePrint.add_url_rule('appliance/logging/forwarding', view_func=LoggingService.as_view('LoggingService'))
