from modules.Vcenter import Vcenter
from modules.Connection import Connection
import requests


class TestConnection:
    def test_vcsa_connect(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        assert response.status_code == 200

    def test_login_success(self, setup_vcenter, session_id):
        setup_vcenter.login()
        assert setup_vcenter.con.session_id == session_id

    def test_login_logout_failure(self, param, host, mpw, user, pw):
        vcenter = Vcenter(host, mpw, user, pw)
        connection = Connection(vcenter)
        response = connection.login()
        assert response is False
        response = connection.logout()
        assert response is False

    def test_logout_success(self, setup_vcenter):
        connection = Connection(setup_vcenter)
        response = connection.logout()
        assert response is True
