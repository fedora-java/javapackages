import os
import sys
import json


def get_configs(cfg_paths=None):
    """
    Returns list of dictionaries which represent configuration files.
    """
    if 'JAVACONFDIRS' in os.environ:
        config_paths = os.environ['JAVACONFDIRS'].split(os.pathsep)
    elif cfg_paths:
        config_paths = cfg_paths
    else:
        config_paths = ['%{javaconfdir}']

    configs = []
    for config_path in config_paths:
        try:
            file_path = os.path.join(config_path, 'javapackages-config.json')
            with open(file_path) as config_file:
                configs.append(json.load(config_file))
        except (OSError, IOError):
            print >> sys.stderr, "Unable to open config file {path}".format(path=file_path)
            pass
    return configs


def get_buildroot():
    try:
        buildroot = os.environ['RPM_BUILD_ROOT']
    except KeyError:
        raise Exception("RPM_BUILD_ROOT environment is not set")
    return os.path.abspath(buildroot)


def get_builddir():
    try:
        builddir = os.environ['JAVAPACKAGES_CACHE_DIR']
    except KeyError:
        raise Exception("JAVAPACKAGES_CACHE_DIR environment is not set")
    return os.path.abspath(builddir)
