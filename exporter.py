# import sys
# sys.path.append('.')

import time
from optparse import OptionParser
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from collectors.VmonCollector import VmonCollector
from modules.Vcenter import Vcenter
import os

def parse_params():
    parser = OptionParser()
    parser.add_option("-o", "--port", help="specify exporter (exporter.py) or inventory serving port(inventory.py)",
                      action="store", dest="port")
    parser.add_option("-d", "--debug", help="enable debug", action="store_true", dest="debug", default=False)
    parser.add_option("-c", "--config", help="path to rest config", action="store", dest="config")
    parser.add_option("-m", "--master-password", help="master password to decrypt mpw", action="store", dest="master_password")
    parser.add_option("-a", "--atlas", help="path to atlas config", action="store", dest="atlas")
    parser.add_option("-u", "--user", help="user used with master password", action="store", dest="user")

    (options, args) = parser.parse_args()
    if options.debug:
        print('DEBUG enabled')
        os.environ['DEBUG'] = "1"
    else:
        os.environ['DEBUG'] = "0"


    return options


def run_prometheus_server(port, vcenter):
    start_http_server(int(port))
    REGISTRY.register(VmonCollector(vcenter))
    while True:
        time.sleep(1)

if __name__ == '__main__':
    options = parse_params()
    vcenter = Vcenter(options.atlas, options.master_password, options.user)
    vcenter.get_vcs_from_atlas()
    run_prometheus_server(options.port, vcenter)
