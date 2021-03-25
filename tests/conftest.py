from mockingServer.MockServer import MockServer
from mockingServer.modules.RequestHandler import RequestHandler
from modules.Vcenter import Vcenter
from exporter import run_prometheus_server
from threading import Thread
import pytest
import json
import yaml
import time


def pytest_addoption(parser):
    """Pytest Parameters. Can be customized when you call pytest."""

    parser.addoption('--host', action='store', default='127.0.0.1')
    parser.addoption('--prometheusport', action='store', default='9011')
    parser.addoption('--mpw', action='store', default='Server')
    parser.addoption('--user', action='store', default='Mocking')


@pytest.fixture(scope='session')
def setup_vcenter(request):
    """The global vcenter that we need to manipulate during testing."""

    host = request.config.getoption('--host')
    mpw = request.config.getoption('--mpw')
    user = request.config.getoption('--user')
    vcenter = Vcenter(host, mpw, user, None)
    yield vcenter


@pytest.fixture(scope='session', autouse=True)
def setup_flask_thread():
    """The Mock Server will be started as a thread."""

    mockserver = MockServer()
    thread = Thread(target=mockserver.start_server)
    thread.daemon = True
    thread.start()


@pytest.fixture(scope='session', autouse=True)
def setup_vcsa_thread(setup_vcenter, request):
    """The VCSA Exporter will be startet as a thread."""

    port = request.config.getoption('--prometheusport')
    thread = Thread(target=run_prometheus_server, args=(port, [setup_vcenter]))
    thread.daemon = True
    thread.start()
    # For the CI runner we need to wait a short period of time to boot up the Prometheus server properly.
    time.sleep(0.2)


@pytest.fixture(scope='session')
def setup_vcsa_url(request):
    """To avoid changing the URL throughout the testcases on changing parameters,
    we create a VCSA URL upfront."""

    ip = request.config.getoption('--host')
    port = request.config.getoption('--prometheusport')
    vcsa_url = 'http://' + ip + ':' + port
    yield vcsa_url


@pytest.fixture(scope='class')
def session_id():
    """Provides the MockSessionID for the testcases"""

    mock_session_id = RequestHandler().session_id['value']
    yield mock_session_id


@pytest.fixture(scope='class')
def rest_yaml():
    """Provides the rest.yaml data from the BaseCollector class for the testcases."""

    with open('./rest.yaml') as yaml_file:
        bc_data = yaml.safe_load(yaml_file)
    yield bc_data


@pytest.fixture(scope='class')
def vmon_json():
    """Provides the vcenter (vmon) json data for the testcases."""

    with open("mockingServer/data/vmon.json", 'r') as data:
        vmon_data = json.load(data)
    yield vmon_data


@pytest.fixture(scope='class')
def logging_json():
    """Provides the vcenter (logging) json data for the testcases"""

    with open("mockingServer/data/logging.json", 'r') as data:
        logging_data = json.load(data)
    yield logging_data


def pytest_runtest_logreport(report):
    """The CI runner has a limited character output on screen. Therefore the location string of tests will
    be limited. AssertionErrors will then be visible at the console."""

    report.nodeid = ''
