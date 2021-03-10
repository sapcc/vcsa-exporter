import pytest
from tests.conftest import ServerSetup
from modules.Vcenter import Vcenter
from modules.Connection import Connection


class TestAuthentication(ServerSetup):
    args = (
        "host, mpw, user, pw",
        [
            pytest.param(
                'False', 'Server', 'Mocking', None
            ),
            pytest.param(
                '127.0.0.1', 'False', 'Mocking', None
            ),
            pytest.param(
                '127.0.0.1', 'Server', 'False', None
            )
        ]
    )

    def test_login_success(self, setup_testcase):
        self.vcenter.login()
        assert self.vcenter.con.session_id == 'MockServerSessionID'

    @pytest.mark.parametrize(*args)
    def test_login_failure(self, host, mpw, user, pw):
        vcenter = Vcenter(host, mpw, user, pw)
        connection = Connection(vcenter)
        response = connection.login()
        assert response is False

    def test_logout_success(self, setup_testcase):
        connection = Connection(self.vcenter)
        response = connection.logout()
        assert response is None

    @pytest.mark.parametrize(*args)
    def test_logout_failure(self, host, mpw, user, pw):
        vcenter = Vcenter(host, mpw, user, pw)
        connection = Connection(vcenter)
        response = connection.logout()
        assert response is False or response is None
