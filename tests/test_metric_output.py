import requests
import yaml


class TestMetricOutput:
    def test_vcsa_data_comparison(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)

        with open('tests/vcsa_output_comparison.yaml', 'r') as fp:
            comparison_data = yaml.safe_load(fp)

        for key in comparison_data.keys():
            difference = set(comparison_data[key]).difference(metrics)
            assert len(difference) == 0

    def test_vcenter_backend_down(self, request, setup_vcsa_url, setup_vcenter):
        setup_vcenter.name = 'foobar-vcenter.whatever.domain'
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)
        setup_vcenter.name = request.config.getoption('--host')
        assert len(metrics) == 0

    def test_consecutive_runs(self, setup_vcsa_url):
        max_size = len(requests.get(setup_vcsa_url).text)
        content_size = max_size
        for run in range(0, 2):
            content_size = len(requests.get(setup_vcsa_url).text)
        assert content_size == max_size

    def process_response_data(self, response):
        results = response.text.split('\n')
        metrics = set()

        for entry in results:
            if entry.startswith(('vcsa_service_status', 'vcsa_logging_status')):
                metrics.add(entry)

        return metrics
