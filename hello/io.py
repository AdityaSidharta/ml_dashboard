import os
import oyaml as yaml


def read_yaml(file_path):
    path = os.path.join(file_path)
    with open(path, "r") as stream:
        try:
            yaml_file = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise yaml.YAMLError(exc)
    return yaml_file
