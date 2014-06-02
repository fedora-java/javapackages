from pomreader import POMReader, PomLoadingException


class POM(object):
    """
    Class for querying basic information from pom.xml files used by Apache Maven
    """
    def __init__(self, path):
        self.__doc = POMReader.load(path)

    def __str__(self):
        return ":".join([self.groupId, self.artifactId, self.version])

    @property
    def parentGroupId(self):
        """
        groupId of the parent artifact or None
        """
        gId = POMReader.find(self.__doc, './pom:parent/pom:groupId')
        if gId is None:
            return None
        else:
            return gId.text.strip()

    @property
    def parentArtifactId(self):
        """
        artifactId of the parent artifact or None
        """
        aId = POMReader.find(self.__doc, './pom:parent/pom:artifactId')
        if aId is None:
            return None
        else:
            return aId.text.strip()

    @property
    def parentVersion(self):
        """
        version of the parent artifact or None
        """
        ver = POMReader.find(self.__doc, './pom:parent/pom:version')
        if ver is None:
            return None
        else:
            return ver.text.strip()

    @property
    def groupId(self):
        """
        Effective groupId of the pom Artifact taking into account parent groupId
        """
        gId = POMReader.find(self.__doc, './pom:groupId')
        if gId is None:
            gId = POMReader.find(self.__doc, './pom:parent/pom:groupId')
        if gId is None:
            gId = POMReader.find(self.__doc, '/ivy-module/info')
            if gId is not None:
                gId = gId.attrib["organisation"]
            if gId is not None:
                return gId
        if gId is None:
            raise PomLoadingException("Unable to determine groupId")
        if len(gId) != 0:
            raise PomLoadingException("Unexpected child nodes under groupId")
        return gId.text.strip()

    @property
    def artifactId(self):
        """
        Effective artifactId of the pom Artifact
        """
        aId = POMReader.find(self.__doc, './pom:artifactId')
        if aId is None:
            aId = POMReader.find(self.__doc, '/ivy-module/info')
            if aId is not None:
                aId = aId.attrib["module"]
            if aId is not None:
                return aId
        if aId is None:
            raise PomLoadingException("Unable to determine artifactID")
        if len(aId) != 0:
            raise PomLoadingException("Unexpected child nodes under artifactId")
        return aId.text.strip()

    @property
    def version(self):
        """
        Effective version of the pom Artifact taking into account parent
        version
        """
        version = POMReader.find(self.__doc, './pom:version')
        if version is None:
            version = POMReader.find(self.__doc, './pom:parent/pom:version')
        if version is None:
            version = POMReader.find(self.__doc, '/ivy-module/info')
            if version is not None:
                version = version.attrib["revision"]
            if version is not None:
                return version
        if version is None:
            raise PomLoadingException("Unable to determine artifact version")
        if len(version) != 0:
            raise PomLoadingException("Unexpected child nodes under version")
        return version.text.strip()

    @property
    def packaging(self):
        """
        Packaging type of artifact or None if unspecified
        """
        p = POMReader.find(self.__doc, './pom:packaging')
        if p is not None:
            if len(p) != 0:
                raise PomLoadingException("Unexpected child nodes under packaging")
            return p.text.strip()
        p = POMReader.find(self.__doc, '/ivy-module/info')
        if p is not None:
            return 'ivy'
        return None
