from modules.Connection import Connection
import requests


class TestConnection:
    def test_vcsa_connect(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        assert response.status_code == 200, 'Response code 200 from the vcsa-exporter expected!'

    def test_login_success(self, setup_vcenter, session_id):
        setup_vcenter.login()
        assert setup_vcenter.con.session_id == session_id,\
            'After a login the presence of the correct session ID is expected.'

    def test_logout_success(self, setup_vcenter):
        connection = Connection(setup_vcenter)
        response = connection.logout()
        assert response is True, 'Expected the response "True" for a successful logout.'

    def test_login_failure(self, setup_vcenter):
        connection = Connection(setup_vcenter)
        connection.pw = 'False'
        response = connection.login()
        assert response is False, 'Expected the response "False" for a failed login.'

    def test_logout_failure(self, setup_vcenter):
        connection = Connection(setup_vcenter)
        connection.pw = 'False'
        response = connection.logout()
        assert response is False, 'Expected the response "False" for a failed logout.'
