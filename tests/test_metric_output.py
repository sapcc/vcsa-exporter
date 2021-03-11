import requests
import yaml


class TestGeneralOutput:
    def test_vcsa_data_comparison(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)

        with open('tests/vcsa_output_comparison.yaml', 'r') as fp:
            comparison_data = yaml.safe_load(fp)

        for key in comparison_data.keys():
            difference = set(comparison_data[key]).difference(metrics)
            assert len(difference) == 0

    def test_vcenter_backend_down(self, request, setup_vcsa_url, setup_vcenter):
        setup_vcenter.name = 'false'
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)
        assert len(metrics) != 0
        setup_vcenter.name = request.config.getoption('--host')

    def process_response_data(self, response):
        results = response.text.split('\n')
        metrics = set()

        for entry in results:
            if entry.startswith('vcsa_service_status') or entry.startswith('vcsa_logging_status'):
                metrics.add(entry)

        return metrics
