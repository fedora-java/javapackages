import javapackages.common.config as config
from javapackages.metadata.metadata import Metadata, MetadataLoadingException
from javapackages.cache.cache import Cache


class MetadataCache(Cache):
    def __init__(self, cachedir, scl=None):
        self._cachedir = cachedir
        self._scl = scl
        self._config_name = config.metadata_cache_f
        self._cache = self._read_cache()

        if self._cache is None:
            self._cache = self._process_buildroot()
            self._write_cache(self._cache)

    def _process_buildroot(self):
        # "path: Metadata" mapping
        cache = {}

        metadata_paths = self._find_paths()
        for path in metadata_paths:
            try:
                metadata = Metadata(path)
                if metadata:
                    cache.update({path: metadata})
            except MetadataLoadingException:
                continue

        return cache

    def _check_path(self, path):
        # TODO
        if "/usr/share/maven-metadata/" in path and path.endswith(".xml"):
            return True
        return False

    def get_artifact_for_path(self, path, can_be_dir=False):
        for metadata in self._cache:
            artifact = metadata.get_artifact_for_path(path,
                                                      can_be_dir=can_be_dir)
            if artifact:
                return artifact
        return None

    def get_metadata_for_path(self, path):
        try:
            return self._cache[path]
        except KeyError:
            pass
        return None

    def get_provided_artifacts(self):
        artifacts = []
        for metadata in self._cache.values():
            artifacts.extend(metadata.artifacts)
        return artifacts

    def get_skipped_artifacts(self):
        artifacts = []
        for metadata in self._cache.values():
            artifacts.extend(metadata.skipped_artifacts)
        return artifacts

    def get_provided_osgi(self):
        bundles = []
        for metadata in self._cache.values():
            bundles += metadata.get_osgi_provides()
        return bundles
