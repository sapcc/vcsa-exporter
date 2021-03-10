import pytest
from threading import Thread
from mockingServer.MockServer import MockServer
from modules.Vcenter import Vcenter
from exporter import run_prometheus_server


@pytest.fixture(scope='session', autouse=True)
def flask_thread():
    mockserver = MockServer()
    thread = Thread(target=mockserver.start_server)
    thread.daemon = True
    thread.start()


@pytest.fixture(scope='session', autouse=True)
def setup_prometheus_thread():
    vCenterList = [Vcenter('127.0.0.1', 'Server', 'Mocking', None)]
    thread = Thread(target=run_prometheus_server, args=(9011, vCenterList))
    thread.daemon = True
    thread.start()


class ServerSetup:
    @pytest.fixture
    def setup_testcase(self):
        self.vcenter = Vcenter('127.0.0.1', 'Server', 'Mocking', None)

