import os
import yaml


def get_value_from_yaml(key):
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd)
    conf = "../config.yaml"
    with open(conf, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            return data.get(key)
        except yaml.YAMLError as e:
            print(e)
    os.chdir(cwd)
     
    


