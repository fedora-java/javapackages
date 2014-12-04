import os
import logging
import pickle
import javapackages.common.config as config


class Cache(object):
    def __init__(self, cachedir, scl=None):
        self._cachedir = cachedir
        self._scl = scl

    def _process_buildroot(self):
        cache = {}
        # TODO: implement in subclass
        return cache

    def _find_paths(self):
        buildroot = config.get_buildroot()
        paths = []
        for dirpath, _, filenames in os.walk(buildroot):
            for filename in filenames:
                fpath = os.path.abspath(os.path.join(dirpath, filename))
                if self._check_path(fpath):
                    paths.append(fpath)
        return paths

    def _check_path(self, path):
        # TODO: implement in subclass
        return False

    def _read_cache(self):
        try:
            cachepath = os.path.join(self._cachedir, self._config_name)
            cachefile = open(cachepath, 'rb')
            ppid, cache = pickle.load(cachefile)
            cachefile.close()
            # check if the cache was most likely created during current build
            if ppid != os.getppid():
                logging.warning("Cache in {path} is outdated, skipping"
                                .format(path=cachepath))
                return None
        except IOError:
            return None
        return cache

    def _write_cache(self, cache):
        try:
            cachefile = open(os.path.join(self._cachedir,
                                          self._config_name), 'wb')
            content = (os.getppid(), cache)
            pickle.dump(content, cachefile)
            cachefile.close()
        except IOError:
            return None
        return cache
