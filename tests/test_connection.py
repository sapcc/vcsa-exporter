import pytest
from modules.Vcenter import Vcenter
from modules.Connection import Connection
from mockingServer.modules.RequestHandler import RequestHandler
import requests


class TestConnection:
    args = (
        "host, mpw, user, pw",
        [
            pytest.param('False', 'Server', 'Mocking', None),
            pytest.param('127.0.0.1', 'False', 'Mocking', None),
            pytest.param('127.0.0.1', 'Server', 'False', None)
        ]
    )

    def test_vcsa_connect(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        assert response.status_code == 200

    def test_login_success(self, setup_vcenter):
        mock_session_id = RequestHandler().session_id['value']
        setup_vcenter.login()
        assert setup_vcenter.con.session_id == mock_session_id

    @pytest.mark.parametrize(*args)
    def test_login_logout_failure(self, host, mpw, user, pw):
        vcenter = Vcenter(host, mpw, user, pw)
        connection = Connection(vcenter)
        response = connection.login()
        assert response is False
        response = connection.logout()
        assert response is False or response is None

    def test_logout_success(self, setup_vcenter):
        connection = Connection(setup_vcenter)
        response = connection.logout()
        assert response is None
