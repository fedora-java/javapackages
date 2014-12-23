# ./pyxbmetadata.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:cc7c37311c49f3aaf8d407a5a18021140495bbc9
# Generated 2014-10-20 13:34:00.773634 by PyXB version 1.2.4 using Python 3.3.2.final.0
# Namespace http://fedorahosted.org/xmvn/METADATA/2.0.0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:fc7e4988-584c-11e4-af6d-3c970e1833ad')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://fedorahosted.org/xmvn/METADATA/2.0.0', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}PackageMetadata with content type ELEMENT_ONLY
class PackageMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Root element of the metadata file.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PackageMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 15, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpfedorahosted_orgxmvnMETADATA2_0_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0uuid', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 23, 6), )

    
    uuid = property(__uuid.value, __uuid.set, None, '2.0.0+\n            Universally unique identifier of this piece of metadata.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpfedorahosted_orgxmvnMETADATA2_0_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0properties', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 31, 6), )

    
    properties = property(__properties.value, __properties.set, None, '2.0.0+\n            Properties of this piece of metadata.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifacts uses Python identifier artifacts
    __artifacts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifacts'), 'artifacts', '__httpfedorahosted_orgxmvnMETADATA2_0_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0artifacts', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 44, 6), )

    
    artifacts = property(__artifacts.value, __artifacts.set, None, '2.0.0+\n            List of installed artifacts described by this piece of\n            metadata.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}skippedArtifacts uses Python identifier skippedArtifacts
    __skippedArtifacts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts'), 'skippedArtifacts', '__httpfedorahosted_orgxmvnMETADATA2_0_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0skippedArtifacts', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 58, 6), )

    
    skippedArtifacts = property(__skippedArtifacts.value, __skippedArtifacts.set, None, '2.0.0+\n            List of artifacts built but not installed in any package.\n            Useful for detecting broken package dependencies.\n          ')

    _ElementMap.update({
        __uuid.name() : __uuid,
        __properties.name() : __properties,
        __artifacts.name() : __artifacts,
        __skippedArtifacts.name() : __skippedArtifacts
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'PackageMetadata', PackageMetadata)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            Properties of this piece of metadata.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 38, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            List of installed artifacts described by this piece of
            metadata.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 52, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifact uses Python identifier artifact
    __artifact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifact'), 'artifact', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON__httpfedorahosted_orgxmvnMETADATA2_0_0artifact', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 54, 12), )

    
    artifact = property(__artifact.value, __artifact.set, None, None)

    _ElementMap.update({
        __artifact.name() : __artifact
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            List of artifacts built but not installed in any package.
            Useful for detecting broken package dependencies.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 66, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}skippedArtifact uses Python identifier skippedArtifact
    __skippedArtifact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact'), 'skippedArtifact', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON_2_httpfedorahosted_orgxmvnMETADATA2_0_0skippedArtifact', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 68, 12), )

    
    skippedArtifact = property(__skippedArtifact.value, __skippedArtifact.set, None, None)

    _ElementMap.update({
        __skippedArtifact.name() : __skippedArtifact
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}SkippedArtifactMetadata with content type ELEMENT_ONLY
class SkippedArtifactMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Information about artifact which was built, but not installed
        into any package.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SkippedArtifactMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 74, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0groupId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 83, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+\n            Group ID of skipped artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0artifactId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 91, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+\n            Artifact ID of skipped artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_0_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0extension', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 99, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+\n            Extension of skipped artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_0_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0classifier', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 107, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+\n            Classifier of skipped artifact.\n          ')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'SkippedArtifactMetadata', SkippedArtifactMetadata)


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}ArtifactMetadata with content type ELEMENT_ONLY
class ArtifactMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Information about a single artifact.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ArtifactMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 117, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0groupId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 125, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+\n            Group identifier of the artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0artifactId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 133, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+\n            Identifier of the artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0extension', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 141, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+\n            Extension of artifact file.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0classifier', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 149, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+\n            Classifier of the artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0version', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 157, 6), )

    
    version = property(__version.value, __version.set, None, '2.0.0+\n            Artifact version.  This is always upstream version, never\n            compat version nor SYSTEM.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}path uses Python identifier path
    __path = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'path'), 'path', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0path', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 166, 6), )

    
    path = property(__path.value, __path.set, None, '2.0.0+\n            Absolute path to artifact file stored in the local file\n            system.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}namespace uses Python identifier namespace
    __namespace = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namespace'), 'namespace', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0namespace', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 175, 6), )

    
    namespace = property(__namespace.value, __namespace.set, None, '2.0.0+\n            A namespace within which this artifact is stored.  This\n            usually is an identifier of software collection.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0uuid', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 184, 6), )

    
    uuid = property(__uuid.value, __uuid.set, None, '2.0.0+\n            Universally unique identifier of this artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0properties', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 192, 6), )

    
    properties = property(__properties.value, __properties.set, None, '2.0.0+\n            Extra properties of this artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}compatVersions uses Python identifier compatVersions
    __compatVersions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'compatVersions'), 'compatVersions', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0compatVersions', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 205, 6), )

    
    compatVersions = property(__compatVersions.value, __compatVersions.set, None, '2.0.0+\n            Compatibility versions of this artifact.  If the list is\n            empty then this artifact is not considered as\n            compatibility artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}aliases uses Python identifier aliases
    __aliases = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'aliases'), 'aliases', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0aliases', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 220, 6), )

    
    aliases = property(__aliases.value, __aliases.set, None, '2.0.0+\n            Alternative identifiers of the artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}dependencies uses Python identifier dependencies
    __dependencies = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), 'dependencies', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_0_0dependencies', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 233, 6), )

    
    dependencies = property(__dependencies.value, __dependencies.set, None, '2.0.0+\n            List of artifact dependencies.\n          ')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier,
        __version.name() : __version,
        __path.name() : __path,
        __namespace.name() : __namespace,
        __uuid.name() : __uuid,
        __properties.name() : __properties,
        __compatVersions.name() : __compatVersions,
        __aliases.name() : __aliases,
        __dependencies.name() : __dependencies
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'ArtifactMetadata', ArtifactMetadata)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            Extra properties of this artifact.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 199, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            Compatibility versions of this artifact.  If the list is
            empty then this artifact is not considered as
            compatibility artifact.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 214, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON_4_httpfedorahosted_orgxmvnMETADATA2_0_0version', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 216, 12), )

    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __version.name() : __version
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            Alternative identifiers of the artifact.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 227, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}alias uses Python identifier alias
    __alias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'alias'), 'alias', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON_5_httpfedorahosted_orgxmvnMETADATA2_0_0alias', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 229, 12), )

    
    alias = property(__alias.value, __alias.set, None, None)

    _ElementMap.update({
        __alias.name() : __alias
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            List of artifact dependencies.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 240, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}dependency uses Python identifier dependency
    __dependency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dependency'), 'dependency', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON_6_httpfedorahosted_orgxmvnMETADATA2_0_0dependency', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 242, 12), )

    
    dependency = property(__dependency.value, __dependency.set, None, None)

    _ElementMap.update({
        __dependency.name() : __dependency
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}ArtifactAlias with content type ELEMENT_ONLY
class ArtifactAlias (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Alternative artifact identification coordinates.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ArtifactAlias')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 248, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_0_0groupId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 256, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+\n            Group ID of the artifact alias.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_0_0artifactId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 264, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+\n            Artifact ID of the artifact alias.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_0_0extension', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 272, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+\n            Extension of the artifact alias.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_0_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_0_0classifier', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 280, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+\n            Classifier of the artifact alias.\n          ')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'ArtifactAlias', ArtifactAlias)


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}Dependency with content type ELEMENT_ONLY
class Dependency (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Description of dependency artifact.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Dependency')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 290, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0groupId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 298, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+\n            Group ID of the dependency artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0artifactId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 306, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+\n            Artifact ID of the dependency artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0extension', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 314, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+\n            Extension of the dependency artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0classifier', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 322, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+\n            Classifier of the dependency artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}requestedVersion uses Python identifier requestedVersion
    __requestedVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion'), 'requestedVersion', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0requestedVersion', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 330, 6), )

    
    requestedVersion = property(__requestedVersion.value, __requestedVersion.set, None, '2.0.0+\n            Version of the dependency artifact as defined in the main\n            artifact descriptor.  This may be a version range as\n            supported by Aether.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}resolvedVersion uses Python identifier resolvedVersion
    __resolvedVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion'), 'resolvedVersion', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0resolvedVersion', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 340, 6), )

    
    resolvedVersion = property(__resolvedVersion.value, __resolvedVersion.set, None, '2.0.0+\n            Version of the dependency artifact, as resolved during\n            build.  Absence of this field indicates a dependency on\n            default artifact version.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}namespace uses Python identifier namespace
    __namespace = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namespace'), 'namespace', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0namespace', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 350, 6), )

    
    namespace = property(__namespace.value, __namespace.set, None, '2.0.0+\n            A namespace within which this artifact is stored.  This\n            usually is an identifier of software collection.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}exclusions uses Python identifier exclusions
    __exclusions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'exclusions'), 'exclusions', '__httpfedorahosted_orgxmvnMETADATA2_0_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_0_0exclusions', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 359, 6), )

    
    exclusions = property(__exclusions.value, __exclusions.set, None, '2.0.0+\n            List of dependency exclusions.\n          ')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier,
        __requestedVersion.name() : __requestedVersion,
        __resolvedVersion.name() : __resolvedVersion,
        __namespace.name() : __namespace,
        __exclusions.name() : __exclusions
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'Dependency', Dependency)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
            List of dependency exclusions.
          """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 366, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}exclusion uses Python identifier exclusion
    __exclusion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'exclusion'), 'exclusion', '__httpfedorahosted_orgxmvnMETADATA2_0_0_CTD_ANON_7_httpfedorahosted_orgxmvnMETADATA2_0_0exclusion', True, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 368, 12), )

    
    exclusion = property(__exclusion.value, __exclusion.set, None, None)

    _ElementMap.update({
        __exclusion.name() : __exclusion
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.0.0}DependencyExclusion with content type ELEMENT_ONLY
class DependencyExclusion (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Description of artifact excluded from dependency tree.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DependencyExclusion')
    _XSDLocation = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 374, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_DependencyExclusion_httpfedorahosted_orgxmvnMETADATA2_0_0groupId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 382, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+\n            Group ID of the excluded artifact.\n          ')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.0.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_0_0_DependencyExclusion_httpfedorahosted_orgxmvnMETADATA2_0_0artifactId', False, pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 390, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+\n            Artifact ID of the excluded artifact.\n          ')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'DependencyExclusion', DependencyExclusion)


metadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metadata'), PackageMetadata, documentation='2.0.0+\n        Root element of the metadata file.\n      ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 7, 2))
Namespace.addCategoryObject('elementBinding', metadata.name().localName(), metadata)



PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.string, scope=PackageMetadata, documentation='2.0.0+\n            Universally unique identifier of this piece of metadata.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 23, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), CTD_ANON, scope=PackageMetadata, documentation='2.0.0+\n            Properties of this piece of metadata.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 31, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifacts'), CTD_ANON_, scope=PackageMetadata, documentation='2.0.0+\n            List of installed artifacts described by this piece of\n            metadata.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 44, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts'), CTD_ANON_2, scope=PackageMetadata, documentation='2.0.0+\n            List of artifacts built but not installed in any package.\n            Useful for detecting broken package dependencies.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 58, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 23, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 23, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 31, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 31, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 44, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifacts')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 44, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 58, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 58, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 23, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 31, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 44, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 58, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_())
    sub_automata.append(_BuildAutomaton_2())
    sub_automata.append(_BuildAutomaton_3())
    sub_automata.append(_BuildAutomaton_4())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 22, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
PackageMetadata._Automaton = _BuildAutomaton()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 40, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 40, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_5()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifact'), ArtifactMetadata, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 54, 12)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 54, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifact')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 54, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_6()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact'), SkippedArtifactMetadata, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 68, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 68, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 68, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_7()




SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+\n            Group ID of skipped artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 83, 6)))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+\n            Artifact ID of skipped artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 91, 6)))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+\n            Extension of skipped artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 99, 6), unicode_default='jar'))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+\n            Classifier of skipped artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 107, 6), unicode_default=''))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 83, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 83, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 91, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 91, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 99, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 99, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 107, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 107, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 83, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 91, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 99, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 107, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_9())
    sub_automata.append(_BuildAutomaton_10())
    sub_automata.append(_BuildAutomaton_11())
    sub_automata.append(_BuildAutomaton_12())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 82, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SkippedArtifactMetadata._Automaton = _BuildAutomaton_8()




ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Group identifier of the artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 125, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Identifier of the artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 133, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Extension of artifact file.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 141, 6), unicode_default='jar'))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Classifier of the artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 149, 6), unicode_default=''))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Artifact version.  This is always upstream version, never\n            compat version nor SYSTEM.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 157, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'path'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Absolute path to artifact file stored in the local file\n            system.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 166, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namespace'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            A namespace within which this artifact is stored.  This\n            usually is an identifier of software collection.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 175, 6), unicode_default=''))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+\n            Universally unique identifier of this artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 184, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), CTD_ANON_3, scope=ArtifactMetadata, documentation='2.0.0+\n            Extra properties of this artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 192, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'compatVersions'), CTD_ANON_4, scope=ArtifactMetadata, documentation='2.0.0+\n            Compatibility versions of this artifact.  If the list is\n            empty then this artifact is not considered as\n            compatibility artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 205, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'aliases'), CTD_ANON_5, scope=ArtifactMetadata, documentation='2.0.0+\n            Alternative identifiers of the artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 220, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), CTD_ANON_6, scope=ArtifactMetadata, documentation='2.0.0+\n            List of artifact dependencies.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 233, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 125, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 125, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 133, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 133, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 141, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 141, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 149, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 149, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 157, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 157, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 166, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'path')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 166, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 175, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namespace')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 175, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 184, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 184, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 192, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 192, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 205, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'compatVersions')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 205, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 220, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'aliases')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 220, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 233, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dependencies')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 233, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 125, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 133, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 141, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 149, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 157, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 166, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 175, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 184, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 192, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 205, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 220, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 233, 6))
    counters.add(cc_11)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_14())
    sub_automata.append(_BuildAutomaton_15())
    sub_automata.append(_BuildAutomaton_16())
    sub_automata.append(_BuildAutomaton_17())
    sub_automata.append(_BuildAutomaton_18())
    sub_automata.append(_BuildAutomaton_19())
    sub_automata.append(_BuildAutomaton_20())
    sub_automata.append(_BuildAutomaton_21())
    sub_automata.append(_BuildAutomaton_22())
    sub_automata.append(_BuildAutomaton_23())
    sub_automata.append(_BuildAutomaton_24())
    sub_automata.append(_BuildAutomaton_25())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 124, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ArtifactMetadata._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 201, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 201, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_26()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 216, 12)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 216, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 216, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_27()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'alias'), ArtifactAlias, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 229, 12)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 229, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'alias')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 229, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_28()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dependency'), Dependency, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 242, 12)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 242, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dependency')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 242, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_29()




ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+\n            Group ID of the artifact alias.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 256, 6)))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+\n            Artifact ID of the artifact alias.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 264, 6)))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+\n            Extension of the artifact alias.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 272, 6), unicode_default='jar'))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+\n            Classifier of the artifact alias.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 280, 6), unicode_default=''))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 256, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 256, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_32 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_32
    del _BuildAutomaton_32
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 264, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 264, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_33 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_33
    del _BuildAutomaton_33
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 272, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 272, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_34 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_34
    del _BuildAutomaton_34
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 280, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 280, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 256, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 264, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 272, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 280, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_31())
    sub_automata.append(_BuildAutomaton_32())
    sub_automata.append(_BuildAutomaton_33())
    sub_automata.append(_BuildAutomaton_34())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 255, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ArtifactAlias._Automaton = _BuildAutomaton_30()




Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Group ID of the dependency artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 298, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Artifact ID of the dependency artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 306, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Extension of the dependency artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 314, 6), unicode_default='jar'))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Classifier of the dependency artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 322, 6), unicode_default=''))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Version of the dependency artifact as defined in the main\n            artifact descriptor.  This may be a version range as\n            supported by Aether.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 330, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            Version of the dependency artifact, as resolved during\n            build.  Absence of this field indicates a dependency on\n            default artifact version.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 340, 6), unicode_default='SYSTEM'))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namespace'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+\n            A namespace within which this artifact is stored.  This\n            usually is an identifier of software collection.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 350, 6), unicode_default=''))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'exclusions'), CTD_ANON_7, scope=Dependency, documentation='2.0.0+\n            List of dependency exclusions.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 359, 6)))

def _BuildAutomaton_36 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 298, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 298, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_37 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_37
    del _BuildAutomaton_37
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 306, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 306, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_38 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_38
    del _BuildAutomaton_38
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 314, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 314, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_39 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_39
    del _BuildAutomaton_39
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 322, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 322, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_40 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_40
    del _BuildAutomaton_40
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 330, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 330, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_41 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_41
    del _BuildAutomaton_41
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 340, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 340, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_42 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_42
    del _BuildAutomaton_42
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 350, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namespace')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 350, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_43 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_43
    del _BuildAutomaton_43
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 359, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'exclusions')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 359, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_35 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_35
    del _BuildAutomaton_35
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 298, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 306, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 314, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 322, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 330, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 340, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 350, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 359, 6))
    counters.add(cc_7)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_36())
    sub_automata.append(_BuildAutomaton_37())
    sub_automata.append(_BuildAutomaton_38())
    sub_automata.append(_BuildAutomaton_39())
    sub_automata.append(_BuildAutomaton_40())
    sub_automata.append(_BuildAutomaton_41())
    sub_automata.append(_BuildAutomaton_42())
    sub_automata.append(_BuildAutomaton_43())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 297, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Dependency._Automaton = _BuildAutomaton_35()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'exclusion'), DependencyExclusion, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 368, 12)))

def _BuildAutomaton_44 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_44
    del _BuildAutomaton_44
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 368, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'exclusion')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 368, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_44()




DependencyExclusion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=DependencyExclusion, documentation='2.0.0+\n            Group ID of the excluded artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 382, 6)))

DependencyExclusion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=DependencyExclusion, documentation='2.0.0+\n            Artifact ID of the excluded artifact.\n          ', location=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 390, 6)))

def _BuildAutomaton_46 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_46
    del _BuildAutomaton_46
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 382, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DependencyExclusion._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 382, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_47 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_47
    del _BuildAutomaton_47
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 390, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DependencyExclusion._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 390, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_45 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_45
    del _BuildAutomaton_45
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 382, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 390, 6))
    counters.add(cc_1)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_46())
    sub_automata.append(_BuildAutomaton_47())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/work-local/projects/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.0.0.xsd', 381, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DependencyExclusion._Automaton = _BuildAutomaton_45()

