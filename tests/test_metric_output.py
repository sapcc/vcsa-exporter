import requests
import yaml
import pytest

class TestMetricOutput:
    def test_prometheus_server_reply(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)

        with open('mockingServer/data/vcsa_output_comparison.yaml', 'r') as fp:
            comparison_data = yaml.safe_load(fp)

        for key in comparison_data.keys():
            difference = set(comparison_data[key]).difference(metrics)
            assert len(difference) == 0, 'No difference between the metric dump and the Prometheus reply expected.'

    def test_backend_recovery_from_down(self, request, setup_vcsa_url, setup_vcenter):
        # Backend up test
        metrics = self.backend_up(setup_vcsa_url)
        assert len(metrics) > 0, 'If the backend is up, vcsa service metrics are expected'
        # Backend down test
        setup_vcenter.name = 'foobar-vcenter.whatever.domain'
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)
        setup_vcenter.name = request.config.getoption('--host')
        assert len(metrics) == 0, 'If the backend is down, no vcsa service metrics are expected'
        # Backend up test
        metrics = self.backend_up(setup_vcsa_url)
        assert len(metrics) > 0, 'If the backend is up after it was down, vcsa service metrics are expected'

    def test_consecutive_runs(self, setup_vcsa_url):
        max_size = len(requests.get(setup_vcsa_url).text)
        content_size = max_size
        for run in range(0, 2):
            content_size = len(requests.get(setup_vcsa_url).text)
        assert content_size == max_size, 'At consecutive runs there is no additional response data expected.'

    """Helper methods for this testcase are located below"""
    def backend_up(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response)
        return metrics

    def process_response_data(self, response):
        results = response.text.split('\n')
        metrics = set()

        for entry in results:
            if entry.startswith(('vcsa_service_status', 'vcsa_logging_status')):
                metrics.add(entry)

        return metrics
