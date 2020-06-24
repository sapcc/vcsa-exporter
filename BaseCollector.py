from abc import ABC, abstractmethod
import yaml

class BaseCollector(ABC):
    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def collect(self):
        pass

    def read_rest_yaml(self):
        with open('./rest.yaml') as yaml_file:
            rest_yaml = yaml.safe_load(yaml_file)
        return rest_yaml
