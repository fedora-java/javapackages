import os
import json


def get_configs():
    """
    Returns list of dictionaries which represent configuration files.
    """
    if 'JAVACONFDIRS' in os.environ:
        config_paths = os.environ['JAVACONFDIRS'].split(os.pathsep)
    else:
        config_paths = ['%{javaconfdir}']

    configs = []
    for config_path in config_paths:
        try:
            file_path = os.path.join(config_path, 'javapackages-config.json')
            with open(file_path) as config_file:
                configs.append(json.load(config_file))
        except (OSError, IOError):
            pass
    return configs
