from modules.Connection import Connection
from BaseCollector import BaseCollector
import pytest
import json
import yaml


@pytest.fixture(scope='class')
def bc_yaml():
    bc_data = BaseCollector.read_rest_yaml()
    yield bc_data


@pytest.fixture(scope='class')
def vmon_json():
    with open("mockingServer/data/vmon.json", 'r') as data:
        vmon_data = json.load(data)
    return vmon_data


@pytest.fixture(scope='class')
def logging_json():
    with open("mockingServer/data/logging.json", 'r') as data:
        logging_data = json.load(data)
    return logging_data


class TestJsonOuput:
    def test_yaml_read(self, bc_yaml):
        with open('./rest.yaml') as yaml_file:
            rest_yaml = yaml.safe_load(yaml_file)
        assert bc_yaml == rest_yaml

    def test_connection_get(self, setup_vcenter, bc_yaml, vmon_json):
        key = bc_yaml['vmonservice']['api_target']
        con = Connection(setup_vcenter)
        response = con.get_request(key)
        assert response is False
        con.login()
        response = con.get_request(key)
        assert vmon_json == response

    def test_connection_post(self, setup_vcenter, bc_yaml, logging_json):
        key = bc_yaml['logging']['api_target']
        data = bc_yaml['logging']['action']
        con = Connection(setup_vcenter)
        response = con.post_request(key, data)
        assert response is False
        con.login()
        response = con.post_request(key, data)
        assert logging_json == response
