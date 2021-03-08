import pytest
from threading import Thread
from mockingServer.MockServer import MockServer
from modules.Vcenter import Vcenter


class ServerSetup:
    @pytest.fixture(scope='class', autouse=True)
    def flask_thread(self):
        thread = Thread(target=self.mocking_server)
        thread.daemon = True
        thread.start()

    def mocking_server(self):
        mockserver = MockServer()
        mockserver.start_server()
