from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.Connection import Connection

class VmonCollector(BaseCollector):
    def __init__(self, vcenter):
        self.vcenter = vcenter

    def describe(self):
        yield GaugeMetricFamily('vcsa_service_status', 'Status of vCSA Services')

    def collect(self):
        for vc in self.vcenter.vcenter_list:
            g = GaugeMetricFamily('vcsa_service_status',
                                  'Status of vCSA Services',
                                   labels=['service', 'health', 'state', 'vccluster'])
            
            rest_yaml = self.read_rest_yaml()
            
            api_target = rest_yaml['vmonservice']['api_target']

            #TODO: move session handling to base class. implement reuse of sessions
            session_id = Connection.login(vc, self.vcenter.user, self.vcenter.generate_pw(vc))
            if not session_id:
                print("skipping vc", vc, ", login not possible")
                continue
            fetched_data = Connection.get_request(vc, api_target, session_id)
            Connection.logout(vc,session_id)
            if not fetched_data:
                print("skipping vc", vc, "fetched data did not return anything")
                continue

            services = dict()
            for service in fetched_data['value']:
                service_name = service['key']
                state = service['value']['state']
                if state != "STARTED":
                    health = "None"
                else:
                    health = service['value']['health']
                metric_value = 1
                if health != 'HEALTHY':
                    metric_value = 0
                g.add_metric(labels=[service_name, health, state, vc], value=metric_value)

            yield g
