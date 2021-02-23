from abc import ABC, abstractmethod
from threading import Thread
import time
import yaml
import logging

LOG = logging.getLogger('vcsa-exporter')


class BaseCollector(ABC):
    def __init__(self, all_vcenters):
        self.metrics = list()
        self.timeout = 60
        self.all_vcenters = all_vcenters

    @abstractmethod
    def describe(self):
        pass

    def collect(self):
        threads = list()
        for vc in self.all_vcenters:
            vc.login()
            if not vc.con.session_id:
                LOG.warning(f"Skipping {vc.name}, did not receive any session id")
                continue
            thread = Thread(target=self.fetch_collector_data, args=(vc,))
            thread.start()
            threads.append((thread, vc.name))

        timeout = self.timeout
        start_time = time.time()
        current_time = start_time
        joined_threads = dict()
        while current_time <= (start_time + timeout):
            for t in threads:
                if not t[0].is_alive():
                    t[0].join()
                    if t[0] not in joined_threads:
                        joined_threads.setdefault(t[1], round(time.time() - start_time))
            if len(joined_threads.keys()) >= len(threads):
                break
            time.sleep(1)
            current_time = time.time()
        else:
            still_running = [t for t in threads if t[0].is_alive()]
            for running_thread in still_running:
                LOG.info(f"Timeout {timeout}s reached for fetching {running_thread[1]}")
                running_thread[0].join(0)
        for vc in joined_threads:
            # self.vrops_collection_times[vrops] = joined_threads[vrops]
            LOG.info(f"Fetched {vc} in {joined_threads[vc]}s")

        for metric in self.metrics:
            yield metric

    @abstractmethod
    def fetch_collector_data(self, vc):
        pass

    @staticmethod
    def read_rest_yaml():
        with open('./rest.yaml') as yaml_file:
            rest_yaml = yaml.safe_load(yaml_file)
        return rest_yaml
