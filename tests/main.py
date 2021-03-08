import pytest
from mockingServer.MockServer import MockServer
from modules.Vcenter import Vcenter
from threading import Thread

"""
@pytest.fixture(scope="session")
def threads():
    t = Thread(target=server)
    t.daemon = True
    t.start()


def server():
    mockserver = MockServer()
    x = Process(target=mockserver.app.run,
                kwargs={"ssl_context": ('..\\mockingServer\\certs\\cert.cert', '..\\mockingServer\\certs\\cert.key'),
                        "port": 443, "debug": False})
    x.run()
"""


@pytest.fixture(scope="session", autouse=True)
def flaskthread():
    thread = Thread(target=server)
    thread.daemon = True
    thread.start()


def server():
    mockserver = MockServer()
    mockserver.start_server()


def test_server():
    vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
    vcenter.login()
    assert vcenter.con.session_id == "MockServerSessionID"


def test_server2():
    vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
    vcenter.login()
    assert vcenter.con.session_id == "MockServerSessionID"


def test_server3():
    vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
    vcenter.login()
    assert vcenter.con.session_id == "MockServerSessionID"