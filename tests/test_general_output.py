from tests.conftest import ServerSetup
import requests
import yaml


class TestGeneralOutput(ServerSetup):
    def test_prometheus_connect(self):
        response = requests.get('http://127.0.0.1:9011')
        assert response.status_code == 200

    def test_vcsa_data_comparison(self):
        response = requests.get('http://127.0.0.1:9011')
        results = response.text.split('\n')
        metrics = set()

        for entry in results:
            if entry.startswith('vcsa_service_status') or entry.startswith('vcsa_logging_status'):
                metrics.add(entry)

        with open('tests/vcsa_output_comparison.yaml', 'r') as fp:
            comparison_data = yaml.safe_load(fp)

        for key in comparison_data.keys():
            difference = set(comparison_data[key]).difference(metrics)
            assert len(difference) == 0
