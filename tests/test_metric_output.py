import requests
import yaml


class TestMetricOutput:
    def test_prometheus_server_reply(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response, metrics=set())

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
        metrics = self.process_response_data(response, metrics=set())
        setup_vcenter.name = request.config.getoption('--host')
        assert len(metrics) == 0, 'If the backend is down, no vcsa service metrics are expected'
        # Backend up test
        metrics = self.backend_up(setup_vcsa_url)
        assert len(metrics) > 0, 'If the backend is up after it was down, vcsa service metrics are expected'

    def test_consecutive_runs(self, setup_vcsa_url):
        max_size = requests.get(setup_vcsa_url)
        max_size = len(self.process_response_data(max_size, metrics=list()))
        content_size = max_size
        for run in range(0, 2):
            content_size = requests.get(setup_vcsa_url)
            content_size = len(self.process_response_data(content_size, metrics=list()))
        assert content_size == max_size, 'At consecutive runs there is no additional response data expected.'

    """Helper methods for this testcase are located below"""
    def backend_up(self, setup_vcsa_url):
        response = requests.get(setup_vcsa_url)
        metrics = self.process_response_data(response, metrics=set())
        return metrics

    def process_response_data(self, response, metrics):
        results = response.text.split('\n')

        for entry in results:
            if entry.startswith(('vcsa_service_status', 'vcsa_logging_status')):
                if isinstance(metrics, set):
                    metrics.add(entry)
                elif isinstance(metrics, list):
                    metrics.append(entry)

        return metrics
