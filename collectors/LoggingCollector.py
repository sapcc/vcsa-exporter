from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.Connection import Connection
import logging

LOG = logging.getLogger('vcsa-exporter')


class LoggingCollector(BaseCollector):
    def __init__(self, vcenter):
        self.vcenter = vcenter
        self.connection_states = {
            'UP': 1,
            'UNKNOWN': 2,
            'DOWN': 0
        }

    def describe(self):
        yield GaugeMetricFamily('vcsa_logging_status', 'Checks the log forwarding of vCSA.')

    def collect(self):
        for vc in self.vcenter.vcenter_list:
            g = GaugeMetricFamily('vcsa_logging_status',
                                  'Checks the log forwarding of vCSA. Down: 0 Up: 1 Unknown: 2',
                                  labels=['loghost', 'vccluster'])

            rest_yaml = self.read_rest_yaml()
            api_target = rest_yaml['logging']['api_target']
            action = rest_yaml['logging']['action']
            session_id = Connection.login(vc, self.vcenter.user, self.vcenter.generate_pw(vc))
            if not session_id:
                LOG.warning(f"skipping vc {vc} login not possible")
                continue
            fetched_data = Connection.post_request(vc, api_target, action, session_id)
            Connection.logout(vc, session_id)
            if not fetched_data:
                LOG.debug(f"skipping vc {vc} fetched data did not return anything")
                continue

            for loghost in fetched_data['value']:
                loghost_name = loghost['hostname']
                state = loghost['state']
                g.add_metric(labels=[loghost_name, vc],
                             value=self.connection_states[state])

            yield g
