import pytest
from tests.ServerSetup import ServerSetup
from modules.Vcenter import Vcenter
from modules.Connection import Connection


class TestAuthorization(ServerSetup):
    args = (
        "host, pw, user, mpw",
        [
            pytest.param(
                'False', None, 'Mocking', 'Nula8.VeyuCaru'
            ),
            pytest.param(
                '127.0.0.1', None, 'False', 'Nula8.VeyuCaru'
            ),
            pytest.param(
                '127.0.0.1', None, 'Mocking', 'False'
            )
        ]
    )

    @pytest.fixture
    def setup_testcase(self):
        self.vcenter = Vcenter('127.0.0.1', None, 'Mocking', 'Nula8.VeyuCaru')

    def test_login_success(self, setup_testcase):
        self.vcenter.login()
        assert self.vcenter.con.session_id == 'MockServerSessionID'

    @pytest.mark.parametrize(*args)
    def test_login_failure(self, host, pw, user, mpw):
        vcenter = Vcenter(host, pw, user, mpw)
        connection = Connection(vcenter)
        response = connection.login()
        assert response is False

    def test_logout_success(self, setup_testcase):
        connection = Connection(self.vcenter)
        response = connection.logout()
        assert response is None

    @pytest.mark.parametrize(*args)
    def test_logout_failure(self, host, pw, user, mpw):
        vcenter = Vcenter(host, pw, user, mpw)
        connection = Connection(vcenter)
        response = connection.logout()
        assert response is False
