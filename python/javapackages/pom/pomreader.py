from lxml.etree import ElementTree, XMLParser


class PomLoadingException(Exception):
    pass


class POMReader(object):

    POM_NAMESPACE = "http://maven.apache.org/POM/4.0.0"

    @staticmethod
    def load(pom_path):
        et = ElementTree()
        parser = XMLParser(remove_comments=True, strip_cdata=True)
        try:
            doc = et.parse(pom_path, parser=parser)
        except IOError:
            raise PomLoadingException("Cannot read file {0}".format(pom_path))

        if doc is None:
            raise PomLoadingException("Failed to load pom.xml")
        return doc

    @staticmethod
    def find(doc, xpath, namespace=POM_NAMESPACE):
        ret = POMReader.xpath(doc, xpath, namespace)
        if len(ret) > 0:
            ret = ret[0]
        else:
            ret = None
        return ret

    @staticmethod
    def xpath(doc, xpath, namespace=POM_NAMESPACE):
        ret = doc.xpath(xpath, namespaces=dict(pom=namespace))
        # perhaps there is no namespace?
        if len(ret) == 0:
            ret = doc.xpath(xpath.replace('pom:', ''))
        return ret
