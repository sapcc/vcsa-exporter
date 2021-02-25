from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.Connection import Connection
import logging

LOG = logging.getLogger('vcsa-exporter')


class LoggingCollector(BaseCollector):
    def __init__(self, all_vcenters):
        super().__init__(all_vcenters)
        self.connection_states = {
            'UP': 1,
            'UNKNOWN': 2,
            'DOWN': 0
        }

    def describe(self):
        yield GaugeMetricFamily('vcsa_logging_status', 'Checks the log forwarding of vCSA.')

    def fetch_collector_data(self, vc):
        g = GaugeMetricFamily('vcsa_logging_status',
                              'Checks the log forwarding of vCSA. Down: 0 Up: 1 Unknown: 2',
                              labels=['loghost', 'vccluster'])

        rest_yaml = BaseCollector.read_rest_yaml()
        api_target = rest_yaml['logging']['api_target']
        action = rest_yaml['logging']['action']
        fetched_data = vc.con.post_request(api_target, action)
        vc.logout()
        if not fetched_data:
            LOG.debug(f"Skipping vc {vc.name} fetched data did not return anything")
            return

        for loghost in fetched_data['value']:
            loghost_name = loghost['hostname']
            state = loghost['state']
            g.add_metric(labels=[loghost_name, vc.name],
                         value=self.connection_states[state])
        self.metrics.append(g)
