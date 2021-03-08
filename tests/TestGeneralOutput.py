from tests.ServerSetup import ServerSetup
from exporter import run_prometheus_server
#from exporter import all_vcenters
from modules.Vcenter import Vcenter
from threading import Thread
import http.client

"""
class TestGeneralOutputTest(ServerSetup):
    def test_collector_metrics(self):
        vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
        all_vcenters = [vcenter]
        thread = Thread(target=run_prometheus_server(9011, all_vcenters))
        thread.daemon = True
        thread.start()
        client = http.client.HTTPConnection("localhost: 9011")
        client.request("GET", "/")
        content = client.getresponse()
        assert content.status == 200
"""

"""
class TestServer(ServerSetup):
    def test_server(self):
        vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
        vcenter.login()
        assert vcenter.con.session_id == "MockServerSessionID"
        print("test1")

    def test_server2(self):
        vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
        vcenter.login()
        assert vcenter.con.session_id == "MockServerSessionID"
        print("test2")

    def test_server3(self):
        vcenter = Vcenter("localhost", None, "Mocking", "Nula8.VeyuCaru")
        vcenter.login()
        assert vcenter.con.session_id == "MockServerSessionID"
"""