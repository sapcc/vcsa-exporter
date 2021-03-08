from mockingServer.modules.RequestHandler import RequestHandler
from flask import Blueprint, make_response
import json

vmonBluePrint = Blueprint('VmonService', import_name=__name__)


class VmonService(RequestHandler):
    def get(self):
        if not self.check_session_id():
            return make_response('sessionID check failed', 401)
        with open("../mockingServer/data/vmon.json", 'r') as data:
            response = json.load(data)
        return response


vmonBluePrint.add_url_rule('/appliance/vmon/service', view_func=VmonService.as_view('VmonService'))
