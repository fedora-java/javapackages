<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:param name="map" /> 
  <xsl:output method="xml" indent="yes" omit-xml-declaration="no"/> 
  <xsl:strip-space elements="*"/> 
  <xsl:template match="/*[name()='project']|/*[name()='model']">

	  <xsl:element name="{name()}">

	  <!-- Replace artifact/group/version/etc. for current project -->

	  <xsl:variable name="artifact" select="./*[name()='artifactId']"/>
	  <xsl:variable name="group" select="./*[name()='groupId']"/>
	  <xsl:variable name="parentGroup" select="./*[name()='parent']/*[name()='groupId']"/>

	  <xsl:choose>
		<xsl:when test="(document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)])">
		  <xsl:for-each select="document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)][1]">
			<xsl:if test="../jpp">
			  <xsl:copy-of select="../jpp/*"/>
			</xsl:if>
		  </xsl:for-each>
		</xsl:when>

		<xsl:otherwise>
		  <xsl:choose>

			<!-- Maybe parent group matches? -->
			<xsl:when test="(document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $parentGroup)])">
			  <xsl:for-each select="document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $parentGroup)][1]">
				<xsl:if test="../jpp">
				  <xsl:copy-of select="../jpp/*"/>
				</xsl:if>
			  </xsl:for-each>
			</xsl:when>

			<!-- Nothing matched -->
			<xsl:otherwise>
			  <xsl:copy-of select="*[name() = 'artifactId']"/>
			  <xsl:copy-of select="*[name() = 'groupId']"/>
			  <xsl:copy-of select="*[name() = 'id']"/>
			  <xsl:copy-of select="*[name() = 'version']"/>
			</xsl:otherwise>
		  </xsl:choose>
		</xsl:otherwise>
	  </xsl:choose>

	  <!-- In the parent, replace groupid/artifactid/version-->

	  <xsl:for-each select="./*[name()='parent']">
		<xsl:apply-templates select="."/>
	  </xsl:for-each>

	  <!-- Copy rest -->
	  <xsl:for-each select="./*">
		<xsl:if test="(name() != 'dependencies') and (name() != 'dependencyManagement') and (name() != 'modelVersion') and (name() != 'parent') and (name() != 'build') and (name() != 'profiles') and (name() != 'artifactId') and (name() != 'groupId') and (name() != 'id') and (name() != 'version')">
		  <xsl:copy-of select="." />
		</xsl:if>
	  </xsl:for-each>

	<!-- If no dependencies exist, add just the <add> items -->
	  <xsl:if test="not(./*[name()='dependencies'])">
		<xsl:element name="dependencies">
		  <xsl:for-each select="document($map)//add/dependency">
			<xsl:copy-of select="." />
		  </xsl:for-each>
		</xsl:element>
	  </xsl:if>

	  <!-- Do not remove this! Maven code has a string match for
	       "<modelVersion>4.0.0" which fails if the line below is
	       removed (because without it, the ns attribute would be
	       added to the modelVersion tag) -->

	  <xsl:for-each select="./*[name()='modelVersion']">
		<xsl:element name="{name()}">
		  <xsl:value-of select="text()" />
		</xsl:element>
	  </xsl:for-each>

	  <!-- Apply templates to rest -->
	  <xsl:apply-templates select="*[name()='build']"/>
	  <xsl:apply-templates select="*[name()='profiles']"/>
	  <xsl:apply-templates select="*[name()='dependencies']"/>
	  <xsl:element name="dependencyManagement">
		<xsl:for-each select="*[name()='dependencyManagement']">
		  <xsl:apply-templates select="*[name()='dependencies']"/>
		</xsl:for-each>
	  </xsl:element>
	</xsl:element>
  </xsl:template>

  <!-- In each of the dependencies, update groupid/artifactid/version -->
  <xsl:template match="*[name()='dependencies']">
	<xsl:element name="dependencies">
	  <xsl:for-each select="*[name()='dependency']">
		<xsl:if test="*[name()='artifactId']">
		  <xsl:call-template name="replace">
			<xsl:with-param name="artifact" select="*[name()='artifactId']/text()"/>
			<xsl:with-param name="group" select="*[name()='groupId']/text()"/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:if test="*[name()='id']">
		  <xsl:choose>
			<xsl:when test="substring-after(*[name()='id']/text(),':') != ''">
			  <xsl:call-template name="replace">
				<xsl:with-param name="artifact" select="substring-after(*[name()='id']/text(),':')"/>
			  </xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
			  <xsl:call-template name="replace">
				<xsl:with-param name="artifact" select="*[name()='id']/text()"/>
			  </xsl:call-template>
			</xsl:otherwise>
		  </xsl:choose>
		</xsl:if>
		<xsl:if test="not(*[name()='artifactId'])">
		  <xsl:copy-of select="."/>
		</xsl:if>
	  </xsl:for-each>
	  <xsl:for-each select="document($map)//add/dependency">
		<xsl:copy-of select="."/>
	  </xsl:for-each>
	</xsl:element>
  </xsl:template>

  <!-- Standard replacement template for dependencies -->

  <xsl:template name="replace">
	<xsl:param name="artifact"/>
	<xsl:param name="group"/>
	<xsl:variable name="this" select="."/>
	  <xsl:choose>
		<xsl:when test="(document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)])">
		  <xsl:for-each select="document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)][1]">
			<xsl:if test="../jpp">
			  <xsl:element name="dependency">
				<xsl:copy-of select="../jpp/*"/>
				<xsl:for-each select="$this/*">
				  <xsl:if test="(name() != 'groupId') and (name() != 'artifactId') and (name() != 'id') and (name() != 'version')">
					<xsl:copy-of select="."/>
				  </xsl:if>
				</xsl:for-each>
			  </xsl:element>
			</xsl:if>
		  </xsl:for-each>
		</xsl:when>
		<xsl:otherwise>
		  <xsl:element name="dependency">
			<xsl:copy-of select="./*"/>
		  </xsl:element>
		</xsl:otherwise>
	  </xsl:choose>
	<xsl:if test="document($map)//dependency/maven[./artifactId/text() = $artifact]">
	  <xsl:for-each select="document($map)//dependency/maven[./artifactId/text() = $artifact][1]">
		<xsl:for-each select="../add/dependency">
		  <xsl:element name="dependency">
			<xsl:copy-of select="./*"/>
		  </xsl:element>
		</xsl:for-each>
	  </xsl:for-each>
	</xsl:if>
  </xsl:template>

  <!-- In the parent, replace groupid/artifactid/version-->

  <xsl:template match="*[name()='parent']">
	<xsl:element name="parent">
	  <xsl:for-each select=".">
		<xsl:if test="*[name()='artifactId']">
		  <xsl:call-template name="replaceNonDep">
			<xsl:with-param name="artifact" select="*[name()='artifactId']/text()"/>
			<xsl:with-param name="group" select="*[name()='groupId']/text()"/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:if test="*[name()='id']">
		  <xsl:choose>
			<xsl:when test="substring-after(*[name()='id']/text(),':') != ''">
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="substring-after(*[name()='id']/text(),':')"/>
			  </xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="*[name()='id']/text()"/>
			  </xsl:call-template>
			</xsl:otherwise>
		  </xsl:choose>
		</xsl:if>
		<xsl:if test="not(*[name()='artifactId'])">
		  <xsl:copy-of select="."/>
		</xsl:if>
	  </xsl:for-each>
	</xsl:element>
  </xsl:template>

  <!-- In build element, replace plugin and extension groupid/artifactid/version -->
  <xsl:template match="*[name()='build']">
	<xsl:element name="build">
	  <xsl:for-each select="./*">
		<xsl:choose>
		  <xsl:when test="(name() != 'plugins') and (name() != 'extensions')">
			<xsl:copy-of select="." />
		  </xsl:when>
		  <xsl:otherwise>
			<xsl:apply-templates select="."/>
		  </xsl:otherwise>
		</xsl:choose>
	  </xsl:for-each>
	</xsl:element>
  </xsl:template>

  <!-- Go through profiles and apply build replacement templates -->
  <xsl:template match="*[name()='profiles']">
	<xsl:element name="profiles">
	  <xsl:for-each select="./*">
		<xsl:choose>
		  <xsl:when test="name() != 'profile'">
			<xsl:copy-of select="." />
		  </xsl:when>
		  <xsl:otherwise>
			<xsl:element name="profile">
			  <xsl:for-each select="./*">
				<xsl:choose>
				  <xsl:when test="(name() != 'build') and (name() != 'dependencies')">
					<xsl:copy-of select="." />
				  </xsl:when>
				  <xsl:otherwise>
					<xsl:apply-templates select="."/>
				  </xsl:otherwise>
				</xsl:choose>
			  </xsl:for-each>
			</xsl:element>
		  </xsl:otherwise>
		</xsl:choose>
	  </xsl:for-each>
	</xsl:element>
  </xsl:template>

  <!-- In plugin info, update groupid/artifactid/version -->
  <xsl:template match="*[name()='plugins']">
	<xsl:element name="plugins">
	  <xsl:for-each select="*[name()='plugin']">
		<xsl:element name="plugin">
		<xsl:if test="*[name()='artifactId']">

		  <xsl:variable name="group">
			<xsl:choose>
			  <xsl:when test="*[name()='groupId']"><xsl:value-of select="*[name()='groupId']/text()"/></xsl:when>
			  <xsl:otherwise>org.apache.maven.plugins<xsl:element name="org.apache.maven.plugins"/></xsl:otherwise>
			</xsl:choose>
		  </xsl:variable>

		  <xsl:call-template name="replaceNonDep">
			<xsl:with-param name="artifact" select="*[name()='artifactId']/text()"/>
			<xsl:with-param name="group" select="$group"/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:if test="*[name()='id']">
		  <xsl:choose>
			<xsl:when test="substring-after(*[name()='id']/text(),':') != ''">
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="substring-after(*[name()='id']/text(),':')"/>
			  </xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="*[name()='id']/text()"/>
			  </xsl:call-template>
			</xsl:otherwise>
		  </xsl:choose>
		</xsl:if>
		<xsl:if test="not(*[name()='artifactId'])">
		  <xsl:copy-of select="."/>
		</xsl:if>
		</xsl:element>
	  </xsl:for-each>

	  <xsl:for-each select="*[name()!='plugin']">
		<xsl:copy-of select="."/>
	  </xsl:for-each>

	</xsl:element>
  </xsl:template>

  <!-- In extension info, update groupid/artifactid/version -->
  <xsl:template match="*[name()='extensions']">
	<xsl:element name="extensions">
	  <xsl:for-each select="*[name()='extension']">
		<xsl:element name="extension">
		<xsl:if test="*[name()='artifactId']">
		  <xsl:call-template name="replaceNonDep">
			<xsl:with-param name="artifact" select="*[name()='artifactId']/text()"/>
			<xsl:with-param name="group" select="*[name()='groupId']/text()"/>
		  </xsl:call-template>
		</xsl:if>
		<xsl:if test="*[name()='id']">
		  <xsl:choose>
			<xsl:when test="substring-after(*[name()='id']/text(),':') != ''">
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="substring-after(*[name()='id']/text(),':')"/>
			  </xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
			  <xsl:call-template name="replaceNonDep">
				<xsl:with-param name="artifact" select="*[name()='id']/text()"/>
			  </xsl:call-template>
			</xsl:otherwise>
		  </xsl:choose>
		</xsl:if>
		<xsl:if test="not(*[name()='artifactId'])">
		  <xsl:copy-of select="."/>
		</xsl:if>
		</xsl:element>
	  </xsl:for-each>

	  <xsl:for-each select="*[name()!='extension']">
		<xsl:copy-of select="."/>
	  </xsl:for-each>

	</xsl:element>
  </xsl:template>

  <!-- Standard template for replacing items that are not <dependency> items -->
  <xsl:template name="replaceNonDep">
	<xsl:param name="artifact"/>
	<xsl:param name="group"/>

	<xsl:variable name="this" select="."/>
	  <xsl:choose>
		<xsl:when test="(document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)])">
		  <xsl:for-each select="document($map)//dependency/maven[(./artifactId/text() = $artifact) and (./groupId/text() = $group)][1]">
			<xsl:if test="../jpp">
			  <xsl:copy-of select="../jpp/*"/>
			  <xsl:for-each select="$this/*">
				<xsl:if test="(name() != 'groupId') and (name() != 'artifactId') and (name() != 'id') and (name() != 'version')">
					<xsl:choose>
						<xsl:when test="name()='dependencies'">
							<xsl:apply-templates select="."/>
						</xsl:when>
						<xsl:otherwise>
						  <xsl:copy-of select="."/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>
			  </xsl:for-each>
			</xsl:if>
		  </xsl:for-each>
		</xsl:when>
		<xsl:otherwise>
			<xsl:for-each select="./*">
				<xsl:choose>
					<xsl:when test="name()='dependencies'">
						<xsl:apply-templates select="."/>
					</xsl:when>
					<xsl:otherwise>
					  <xsl:copy-of select="."/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
		</xsl:otherwise>
	  </xsl:choose>
  </xsl:template>


</xsl:stylesheet>
