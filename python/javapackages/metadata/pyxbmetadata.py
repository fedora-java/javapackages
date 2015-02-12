# ./javapackages/metadata/pyxbmetadata.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c6f1fde6e140d7c95c44b8f773742fbcefa7ed69
# Generated 2015-02-12 12:30:35.748334 by PyXB version 1.2.4 using Python 3.4.1.final.0
# Namespace http://fedorahosted.org/xmvn/METADATA/2.3.0

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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:8feaf11e-b2aa-11e4-bf2a-0024d7e4685c')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://fedorahosted.org/xmvn/METADATA/2.3.0', create_if_missing=True)
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


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}PackageMetadata with content type ELEMENT_ONLY
class PackageMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+
        Root element of the metadata file.
      """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PackageMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 15, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpfedorahosted_orgxmvnMETADATA2_3_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0uuid', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 23, 6), )

    
    uuid = property(__uuid.value, __uuid.set, None, '2.0.0+Universally unique identifier of this piece of metadata.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpfedorahosted_orgxmvnMETADATA2_3_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0properties', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 29, 6), )

    
    properties = property(__properties.value, __properties.set, None, '2.0.0+Properties of this piece of metadata.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifacts uses Python identifier artifacts
    __artifacts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifacts'), 'artifacts', '__httpfedorahosted_orgxmvnMETADATA2_3_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0artifacts', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 40, 6), )

    
    artifacts = property(__artifacts.value, __artifacts.set, None, '2.0.0+List of installed artifacts described by this piece of metadata.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}skippedArtifacts uses Python identifier skippedArtifacts
    __skippedArtifacts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts'), 'skippedArtifacts', '__httpfedorahosted_orgxmvnMETADATA2_3_0_PackageMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0skippedArtifacts', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 51, 6), )

    
    skippedArtifacts = property(__skippedArtifacts.value, __skippedArtifacts.set, None, '2.0.0+List of artifacts built but not installed in any package. Useful for detecting broken package dependencies.')

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
    """2.0.0+Properties of this piece of metadata."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 34, 8)
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
    """2.0.0+List of installed artifacts described by this piece of metadata."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 45, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifact uses Python identifier artifact
    __artifact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifact'), 'artifact', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON__httpfedorahosted_orgxmvnMETADATA2_3_0artifact', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 47, 12), )

    
    artifact = property(__artifact.value, __artifact.set, None, None)

    _ElementMap.update({
        __artifact.name() : __artifact
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+List of artifacts built but not installed in any package. Useful for detecting broken package dependencies."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 56, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}skippedArtifact uses Python identifier skippedArtifact
    __skippedArtifact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact'), 'skippedArtifact', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON_2_httpfedorahosted_orgxmvnMETADATA2_3_0skippedArtifact', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 58, 12), )

    
    skippedArtifact = property(__skippedArtifact.value, __skippedArtifact.set, None, None)

    _ElementMap.update({
        __skippedArtifact.name() : __skippedArtifact
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}SkippedArtifactMetadata with content type ELEMENT_ONLY
class SkippedArtifactMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Information about artifact which was built, but not installed into any package."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SkippedArtifactMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 64, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0groupId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 70, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+Group ID of skipped artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0artifactId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 76, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+Artifact ID of skipped artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_3_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0extension', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 82, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+Extension of skipped artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_3_0_SkippedArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0classifier', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 88, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+Classifier of skipped artifact.')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'SkippedArtifactMetadata', SkippedArtifactMetadata)


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}ArtifactMetadata with content type ELEMENT_ONLY
class ArtifactMetadata (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Information about a single artifact."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ArtifactMetadata')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 96, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0groupId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 102, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+Group identifier of the artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0artifactId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 108, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+Identifier of the artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0extension', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 114, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+Extension of artifact file.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0classifier', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 120, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+Classifier of the artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0version', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 126, 6), )

    
    version = property(__version.value, __version.set, None, '2.0.0+Artifact version. This is always upstream version, never compat version nor SYSTEM.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}path uses Python identifier path
    __path = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'path'), 'path', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0path', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 132, 6), )

    
    path = property(__path.value, __path.set, None, '2.0.0+Absolute path to artifact file stored in the local file system.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}namespace uses Python identifier namespace
    __namespace = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namespace'), 'namespace', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0namespace', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 138, 6), )

    
    namespace = property(__namespace.value, __namespace.set, None, '2.0.0+A namespace within which this artifact is stored. This usually is an identifier of software collection.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}uuid uses Python identifier uuid
    __uuid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'uuid'), 'uuid', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0uuid', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 144, 6), )

    
    uuid = property(__uuid.value, __uuid.set, None, '2.0.0+Universally unique identifier of this artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0properties', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 150, 6), )

    
    properties = property(__properties.value, __properties.set, None, '2.0.0+Extra properties of this artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}compatVersions uses Python identifier compatVersions
    __compatVersions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'compatVersions'), 'compatVersions', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0compatVersions', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 161, 6), )

    
    compatVersions = property(__compatVersions.value, __compatVersions.set, None, '2.0.0+Compatibility versions of this artifact. If the list is empty then this artifact is not considered as compatibility artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}aliases uses Python identifier aliases
    __aliases = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'aliases'), 'aliases', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0aliases', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 172, 6), )

    
    aliases = property(__aliases.value, __aliases.set, None, '2.0.0+Alternative identifiers of the artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}dependencies uses Python identifier dependencies
    __dependencies = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), 'dependencies', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactMetadata_httpfedorahosted_orgxmvnMETADATA2_3_0dependencies', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 183, 6), )

    
    dependencies = property(__dependencies.value, __dependencies.set, None, '2.0.0+List of artifact dependencies.')

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
    """2.0.0+Extra properties of this artifact."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 155, 8)
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
    """2.0.0+Compatibility versions of this artifact. If the list is empty then this artifact is not considered as compatibility artifact."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 166, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON_4_httpfedorahosted_orgxmvnMETADATA2_3_0version', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 168, 12), )

    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __version.name() : __version
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Alternative identifiers of the artifact."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 177, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}alias uses Python identifier alias
    __alias = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'alias'), 'alias', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON_5_httpfedorahosted_orgxmvnMETADATA2_3_0alias', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 179, 12), )

    
    alias = property(__alias.value, __alias.set, None, None)

    _ElementMap.update({
        __alias.name() : __alias
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+List of artifact dependencies."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 188, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}dependency uses Python identifier dependency
    __dependency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dependency'), 'dependency', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON_6_httpfedorahosted_orgxmvnMETADATA2_3_0dependency', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 190, 12), )

    
    dependency = property(__dependency.value, __dependency.set, None, None)

    _ElementMap.update({
        __dependency.name() : __dependency
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}ArtifactAlias with content type ELEMENT_ONLY
class ArtifactAlias (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Alternative artifact identification coordinates."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ArtifactAlias')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 196, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_3_0groupId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 202, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+Group ID of the artifact alias.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_3_0artifactId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 208, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+Artifact ID of the artifact alias.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_3_0extension', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 214, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+Extension of the artifact alias.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_3_0_ArtifactAlias_httpfedorahosted_orgxmvnMETADATA2_3_0classifier', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 220, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+Classifier of the artifact alias.')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'ArtifactAlias', ArtifactAlias)


# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}Dependency with content type ELEMENT_ONLY
class Dependency (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Description of dependency artifact."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Dependency')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 228, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0groupId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 234, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+Group ID of the dependency artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0artifactId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 240, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+Artifact ID of the dependency artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}extension uses Python identifier extension
    __extension = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'extension'), 'extension', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0extension', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 246, 6), )

    
    extension = property(__extension.value, __extension.set, None, '2.0.0+Extension of the dependency artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}classifier uses Python identifier classifier
    __classifier = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'classifier'), 'classifier', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0classifier', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 252, 6), )

    
    classifier = property(__classifier.value, __classifier.set, None, '2.0.0+Classifier of the dependency artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}requestedVersion uses Python identifier requestedVersion
    __requestedVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion'), 'requestedVersion', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0requestedVersion', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 258, 6), )

    
    requestedVersion = property(__requestedVersion.value, __requestedVersion.set, None, '2.0.0+Version of the dependency artifact as defined in the main artifact descriptor. This may be a version range as supported by Aether.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}resolvedVersion uses Python identifier resolvedVersion
    __resolvedVersion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion'), 'resolvedVersion', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0resolvedVersion', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 264, 6), )

    
    resolvedVersion = property(__resolvedVersion.value, __resolvedVersion.set, None, '2.0.0+Version of the dependency artifact, as resolved during build. Absence of this field indicates a dependency on default artifact version.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}namespace uses Python identifier namespace
    __namespace = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'namespace'), 'namespace', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0namespace', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 270, 6), )

    
    namespace = property(__namespace.value, __namespace.set, None, '2.0.0+A namespace within which this artifact is stored. This usually is an identifier of software collection.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}optional uses Python identifier optional
    __optional = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'optional'), 'optional', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0optional', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 276, 6), )

    
    optional = property(__optional.value, __optional.set, None, '2.3.0+Specifies whether given dependency is optional or not.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}exclusions uses Python identifier exclusions
    __exclusions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'exclusions'), 'exclusions', '__httpfedorahosted_orgxmvnMETADATA2_3_0_Dependency_httpfedorahosted_orgxmvnMETADATA2_3_0exclusions', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 282, 6), )

    
    exclusions = property(__exclusions.value, __exclusions.set, None, '2.0.0+List of dependency exclusions.')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId,
        __extension.name() : __extension,
        __classifier.name() : __classifier,
        __requestedVersion.name() : __requestedVersion,
        __resolvedVersion.name() : __resolvedVersion,
        __namespace.name() : __namespace,
        __optional.name() : __optional,
        __exclusions.name() : __exclusions
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'Dependency', Dependency)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+List of dependency exclusions."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 287, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}exclusion uses Python identifier exclusion
    __exclusion = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'exclusion'), 'exclusion', '__httpfedorahosted_orgxmvnMETADATA2_3_0_CTD_ANON_7_httpfedorahosted_orgxmvnMETADATA2_3_0exclusion', True, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 289, 12), )

    
    exclusion = property(__exclusion.value, __exclusion.set, None, None)

    _ElementMap.update({
        __exclusion.name() : __exclusion
    })
    _AttributeMap.update({
        
    })



# Complex type {http://fedorahosted.org/xmvn/METADATA/2.3.0}DependencyExclusion with content type ELEMENT_ONLY
class DependencyExclusion (pyxb.binding.basis.complexTypeDefinition):
    """2.0.0+Description of artifact excluded from dependency tree."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DependencyExclusion')
    _XSDLocation = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 295, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}groupId uses Python identifier groupId
    __groupId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groupId'), 'groupId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_DependencyExclusion_httpfedorahosted_orgxmvnMETADATA2_3_0groupId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 301, 6), )

    
    groupId = property(__groupId.value, __groupId.set, None, '2.0.0+Group ID of the excluded artifact.')

    
    # Element {http://fedorahosted.org/xmvn/METADATA/2.3.0}artifactId uses Python identifier artifactId
    __artifactId = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), 'artifactId', '__httpfedorahosted_orgxmvnMETADATA2_3_0_DependencyExclusion_httpfedorahosted_orgxmvnMETADATA2_3_0artifactId', False, pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 307, 6), )

    
    artifactId = property(__artifactId.value, __artifactId.set, None, '2.0.0+Artifact ID of the excluded artifact.')

    _ElementMap.update({
        __groupId.name() : __groupId,
        __artifactId.name() : __artifactId
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'DependencyExclusion', DependencyExclusion)


metadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metadata'), PackageMetadata, documentation='2.0.0+\n        Root element of the metadata file.\n      ', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 7, 2))
Namespace.addCategoryObject('elementBinding', metadata.name().localName(), metadata)



PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.string, scope=PackageMetadata, documentation='2.0.0+Universally unique identifier of this piece of metadata.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 23, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), CTD_ANON, scope=PackageMetadata, documentation='2.0.0+Properties of this piece of metadata.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 29, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifacts'), CTD_ANON_, scope=PackageMetadata, documentation='2.0.0+List of installed artifacts described by this piece of metadata.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 40, 6)))

PackageMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts'), CTD_ANON_2, scope=PackageMetadata, documentation='2.0.0+List of artifacts built but not installed in any package. Useful for detecting broken package dependencies.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 51, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 23, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 23, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 29, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 29, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 40, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifacts')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 40, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 51, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(PackageMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifacts')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 51, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 23, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 29, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 40, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 51, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_())
    sub_automata.append(_BuildAutomaton_2())
    sub_automata.append(_BuildAutomaton_3())
    sub_automata.append(_BuildAutomaton_4())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 22, 4)
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
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 36, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 36, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_5()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifact'), ArtifactMetadata, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 47, 12)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 47, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifact')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 47, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_6()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact'), SkippedArtifactMetadata, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 58, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 58, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'skippedArtifact')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 58, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_7()




SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+Group ID of skipped artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 70, 6)))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+Artifact ID of skipped artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 76, 6)))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+Extension of skipped artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 82, 6), unicode_default='jar'))

SkippedArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=SkippedArtifactMetadata, documentation='2.0.0+Classifier of skipped artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 88, 6), unicode_default=''))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 70, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 70, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 76, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 76, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 82, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 82, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 88, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(SkippedArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 88, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 70, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 76, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 82, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 88, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_9())
    sub_automata.append(_BuildAutomaton_10())
    sub_automata.append(_BuildAutomaton_11())
    sub_automata.append(_BuildAutomaton_12())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 69, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
SkippedArtifactMetadata._Automaton = _BuildAutomaton_8()




ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Group identifier of the artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 102, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Identifier of the artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 108, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Extension of artifact file.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 114, 6), unicode_default='jar'))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Classifier of the artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 120, 6), unicode_default=''))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Artifact version. This is always upstream version, never compat version nor SYSTEM.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 126, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'path'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Absolute path to artifact file stored in the local file system.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 132, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namespace'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+A namespace within which this artifact is stored. This usually is an identifier of software collection.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 138, 6), unicode_default=''))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'uuid'), pyxb.binding.datatypes.string, scope=ArtifactMetadata, documentation='2.0.0+Universally unique identifier of this artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 144, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), CTD_ANON_3, scope=ArtifactMetadata, documentation='2.0.0+Extra properties of this artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 150, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'compatVersions'), CTD_ANON_4, scope=ArtifactMetadata, documentation='2.0.0+Compatibility versions of this artifact. If the list is empty then this artifact is not considered as compatibility artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 161, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'aliases'), CTD_ANON_5, scope=ArtifactMetadata, documentation='2.0.0+Alternative identifiers of the artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 172, 6)))

ArtifactMetadata._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), CTD_ANON_6, scope=ArtifactMetadata, documentation='2.0.0+List of artifact dependencies.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 183, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 102, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 102, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 108, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 108, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 114, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 114, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 120, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 120, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 126, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 126, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 132, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'path')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 132, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 138, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namespace')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 138, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 144, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'uuid')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 144, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 150, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 150, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 161, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'compatVersions')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 161, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 172, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'aliases')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 172, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 183, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactMetadata._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dependencies')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 183, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 102, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 108, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 114, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 120, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 126, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 132, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 138, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 144, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 150, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 161, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 172, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 183, 6))
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
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 101, 4)
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
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 157, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_skip, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 157, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_26()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 168, 12)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 168, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 168, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_27()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'alias'), ArtifactAlias, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 179, 12)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 179, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'alias')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 179, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_28()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dependency'), Dependency, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 190, 12)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 190, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dependency')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 190, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_29()




ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+Group ID of the artifact alias.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 202, 6)))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+Artifact ID of the artifact alias.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 208, 6)))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+Extension of the artifact alias.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 214, 6), unicode_default='jar'))

ArtifactAlias._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=ArtifactAlias, documentation='2.0.0+Classifier of the artifact alias.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 220, 6), unicode_default=''))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 202, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 202, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 208, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 208, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 214, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 214, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 220, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ArtifactAlias._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 220, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 202, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 208, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 214, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 220, 6))
    counters.add(cc_3)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_31())
    sub_automata.append(_BuildAutomaton_32())
    sub_automata.append(_BuildAutomaton_33())
    sub_automata.append(_BuildAutomaton_34())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 201, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ArtifactAlias._Automaton = _BuildAutomaton_30()




Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Group ID of the dependency artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 234, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Artifact ID of the dependency artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 240, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'extension'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Extension of the dependency artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 246, 6), unicode_default='jar'))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'classifier'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Classifier of the dependency artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 252, 6), unicode_default=''))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Version of the dependency artifact as defined in the main artifact descriptor. This may be a version range as supported by Aether.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 258, 6), unicode_default='SYSTEM'))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+Version of the dependency artifact, as resolved during build. Absence of this field indicates a dependency on default artifact version.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 264, 6), unicode_default='SYSTEM'))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'namespace'), pyxb.binding.datatypes.string, scope=Dependency, documentation='2.0.0+A namespace within which this artifact is stored. This usually is an identifier of software collection.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 270, 6), unicode_default=''))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'optional'), pyxb.binding.datatypes.boolean, scope=Dependency, documentation='2.3.0+Specifies whether given dependency is optional or not.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 276, 6)))

Dependency._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'exclusions'), CTD_ANON_7, scope=Dependency, documentation='2.0.0+List of dependency exclusions.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 282, 6)))

def _BuildAutomaton_36 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 234, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 234, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 240, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 240, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 246, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'extension')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 246, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 252, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'classifier')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 252, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 258, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'requestedVersion')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 258, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 264, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'resolvedVersion')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 264, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 270, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'namespace')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 270, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 276, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'optional')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 276, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_44 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_44
    del _BuildAutomaton_44
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 282, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Dependency._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'exclusions')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 282, 6))
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
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 234, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 240, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 246, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 252, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 258, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 264, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 270, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 276, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 282, 6))
    counters.add(cc_8)
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
    sub_automata.append(_BuildAutomaton_44())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 233, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Dependency._Automaton = _BuildAutomaton_35()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'exclusion'), DependencyExclusion, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 289, 12)))

def _BuildAutomaton_45 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_45
    del _BuildAutomaton_45
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 289, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'exclusion')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 289, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_45()




DependencyExclusion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groupId'), pyxb.binding.datatypes.string, scope=DependencyExclusion, documentation='2.0.0+Group ID of the excluded artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 301, 6)))

DependencyExclusion._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'artifactId'), pyxb.binding.datatypes.string, scope=DependencyExclusion, documentation='2.0.0+Artifact ID of the excluded artifact.', location=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 307, 6)))

def _BuildAutomaton_47 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_47
    del _BuildAutomaton_47
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 301, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DependencyExclusion._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groupId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 301, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_48 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_48
    del _BuildAutomaton_48
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 307, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DependencyExclusion._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'artifactId')), pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 307, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_46 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_46
    del _BuildAutomaton_46
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 301, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 307, 6))
    counters.add(cc_1)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_47())
    sub_automata.append(_BuildAutomaton_48())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/msimacek/git/xmvn/xmvn-core/target/generated-site/resources/xsd/metadata-2.3.0.xsd', 300, 4)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DependencyExclusion._Automaton = _BuildAutomaton_46()

