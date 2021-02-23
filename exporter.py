#!/usr/bin/python3
from optparse import OptionParser
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from collectors.VmonCollector import VmonCollector
from modules.Vcenter import Vcenter
from collectors.LoggingCollector import LoggingCollector
import time
import logging

LOG = logging.getLogger('vcsa-exporter')


def parse_params(logger):
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ConsoleHandler = logging.StreamHandler()
    logger.addHandler(ConsoleHandler)
    ConsoleHandler.setFormatter(formatter)

    parser = OptionParser()
    parser.add_option("-o", "--port", help="specify exporter (exporter.py) or inventory serving port(inventory.py)",
                      action="store", dest="port")
    parser.add_option("-d", "--debug", help="enable debug", action="store_true", dest="debug", default=False)
    parser.add_option("-v", "--verbose", help="log all level but debug", action="store_true", dest="info", default=False)
    parser.add_option("-c", "--config", help="path to rest config", action="store", dest="config")
    parser.add_option("-m", "--master-password", help="master password to decrypt mpw", action="store", dest="master_password")
    parser.add_option("-a", "--atlas", help="path to atlas config", action="store", dest="atlas")
    parser.add_option("-u", "--user", help="user used with master password", action="store", dest="user")
    parser.add_option("-p", "--password", help="specify password to log in", action="store", dest="password")

    (options, args) = parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        ConsoleHandler.setLevel(logging.DEBUG)
        logger.info('Starting exporter logging on DEBUG level')
    if options.info:
        logger.setLevel(logging.INFO)
        ConsoleHandler.setLevel(logging.INFO)
        logger.info('Starting exporter logging on INFO level')
    if not options.debug and not options.info:
        logger.setLevel(logging.WARNING)
        ConsoleHandler.setLevel(logging.WARNING)
        logger.warning('Starting exporter logging on WARNING, ERROR and CRITICAL level')
    return options


def run_prometheus_server(port, vcenter):
    start_http_server(int(port))
    REGISTRY.register(VmonCollector(all_vcenters))
    REGISTRY.register(LoggingCollector(all_vcenters))
    while True:
        time.sleep(1)


if __name__ == '__main__':
    logger = logging.getLogger('vcsa-exporter')
    options = parse_params(logger)
    all_vcenters = list()
    for vcenter in Vcenter.get_vcs_from_atlas(options.atlas):
        all_vcenters.append(Vcenter(vcenter, options.atlas, options.master_password,
                                    options.user, password=options.password))
    run_prometheus_server(options.port, all_vcenters)
