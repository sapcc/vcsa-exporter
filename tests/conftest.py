from mockingServer.MockServer import MockServer
from modules.Vcenter import Vcenter
from exporter import run_prometheus_server
import pytest
from threading import Thread


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


@pytest.fixture(scope='session')
def setup_vcsa_url(request):
    """To avoid changing the URL throughout the testcases on changing parameters,
    we create a VCSA URL upfront."""

    ip = request.config.getoption('--host')
    port = request.config.getoption('--prometheusport')
    vcsa_url = 'http://' + ip + ':' + port
    yield vcsa_url


@pytest.fixture(scope='session')
def param():
    """The param fixture allows us to pass all parameters from pytest_generate_tests to the target tests."""

    pass


def pytest_generate_tests(metafunc):
    """Parametrize testcases. These can be reused if the testcase implements the parameters listed below"""

    host = metafunc.config.getoption('--host')
    mpw = metafunc.config.getoption('--mpw')
    user = metafunc.config.getoption('--user')

    if 'param' in metafunc.fixturenames:
        metafunc.parametrize("host, mpw, user, pw", [
            pytest.param('False', mpw, user, None),
            pytest.param(host, 'False', user, None),
            pytest.param(host, mpw, 'False', None)
        ])
