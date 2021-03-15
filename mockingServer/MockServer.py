from flask import Flask
from mockingServer.modules.Authentication import authBluePrint
from mockingServer.modules.VmonService import vmonBluePrint
from mockingServer.modules.LoggingSession import loggingBluePrint
from gevent.pywsgi import WSGIServer


class MockServer:
    def __init__(self, port=443):
        self.app = Flask(__name__)
        self.port = port
        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(authBluePrint, url_prefix='/rest')
        self.app.register_blueprint(vmonBluePrint, url_prefix='/rest')
        self.app.register_blueprint(loggingBluePrint, url_prefix='/rest')

    def start_server(self):
        WSGIServer(('localhost', self.port), self.app,
                   keyfile='mockingServer/certs/cert.key',
                   certfile='mockingServer/certs/cert.cert').serve_forever()
