from flask import Blueprint, request, make_response
from mockingServer.modules.RequestHandler import RequestHandler
import master_password

authBluePrint = Blueprint('AuthenticationService', import_name=__name__)


class Authentication(RequestHandler):
    def __init__(self):
        super().__init__()
        self.username = "Mocking"
        self.mpw = "Server"
        self.url = '127.0.0.1'
        self.password = master_password.MPW(self.username, self.mpw).password(self.url).replace('/', '')

    def post(self):
        if not self.login():
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return self.session_id

    def delete(self):
        return make_response('Success', 200)

    def login(self):
        auth = request.authorization
        if auth and self.check_auth(auth.username, auth.password):
            return True
        return False

    def check_auth(self, username, password):
        if username == self.username and password == self.password:
            return True
        return False


authBluePrint.add_url_rule('/com/vmware/cis/session', view_func=Authentication.as_view('Authentication'))
