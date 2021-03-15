from modules.Connection import Connection
from BaseCollector import BaseCollector


class TestJsonOuput:
    def test_yaml_read(self, rest_yaml):
        bc_data = BaseCollector.read_rest_yaml()
        assert rest_yaml == bc_data, 'Identical yaml data expected.'

    def test_connection_get(self, setup_vcenter, rest_yaml, vmon_json):
        api_target = rest_yaml['vmonservice']['api_target']
        con = Connection(setup_vcenter)
        response = con.get_request(api_target)
        assert response is False, 'Response fail expected, because there was no previous login (SessionID missing).'
        con.login()
        response = con.get_request(api_target)
        assert vmon_json == response, 'Identical vmon json data expected.'

    def test_connection_post(self, setup_vcenter, rest_yaml, logging_json):
        api_target = rest_yaml['logging']['api_target']
        data = rest_yaml['logging']['action']
        con = Connection(setup_vcenter)
        response = con.post_request(api_target, data)
        assert response is False, 'Response fail expected, because there was no previous login (SessionID missing).'
        con.login()
        response = con.post_request(api_target, data)
        assert logging_json == response, 'Identical logging json data expected.'
