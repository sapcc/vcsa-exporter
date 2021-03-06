from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
import logging

LOG = logging.getLogger('vcsa-exporter')


class VmonCollector(BaseCollector):
    def __init__(self, all_vcenters):
        super().__init__(all_vcenters)
        self.health_states = {
            "HEALTHY": 3,
            "HEALTHY_WITH_WARNINGS": 2,
            "DEGRADED": 1,
            "STOPPED": 0
        }

    def describe(self):
        yield GaugeMetricFamily('vcsa_service_status', 'Health Status of vCSA Services')

    def fetch_collector_data(self, vc):
        g = GaugeMetricFamily('vcsa_service_status',
                              'Status of vCSA Services',
                              labels=['service', 'vccluster'])

        rest_yaml = BaseCollector.read_rest_yaml()

        api_target = rest_yaml['vmonservice']['api_target']

        fetched_data = vc.con.get_request(api_target)
        vc.logout()
        if not fetched_data:
            LOG.warning(f"skipping vc {vc.name} fetched data did not return anything")
            return

        for service in fetched_data['value']:
            service_name = service['key']
            state = service['value']['state']
            if state == "STOPPED":
                service_health = "STOPPED"
            else:
                service_health = service['value']['health']

            g.add_metric(labels=[service_name, vc.name], value=self.health_states[service_health])
        self.metrics.append(g)
