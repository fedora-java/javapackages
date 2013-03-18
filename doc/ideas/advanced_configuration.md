`maven-local` provides various macros for building and installing
artifacts and for controlling the build process.  These macros are
enough in the great majority of cases, but sometimes there is a need
to have more control over the build process.

XMvn project is the implementation of macros provided by `maven-local`
package.  One way to have more control over the build process is
configuring XMvn directly, without the intermediate layer provides by
`maven-local`.

XMvn configuration is documented on the XMvn site, you can refer to
this documentation.  What is important here is the way of specifying
configuration.  In most cases it's enough to create
`.xmvn/configuration.xml` file in the build directory that contains
the XMvn configuration in XML format.  That file will be loaded
automatically by XMvn.

.Example of specifying custom XMvn configuration
[source,spec]
-------
%prep
...
mkdir -p .xmvn
cat <<EOF >.xmvn/configuration.xml
<configuration>
  <resolverSettings>
    <jarRepositories>
      <repository>/usr/share/some_package/custom-repo</repository>
    </jarRepositories>
  <resolverSettings>
</configuration>
EOF
-------
