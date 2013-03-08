Virtual artifact packages
-------------------------

Each Maven artifact packaged into an RPM package has corresponding
virtual package named `mvn(groupId:artifactId)`, created automatically
by the build system.  If more than one artifact is included in a
physical package then one virtual package is created for each of them.
Virtual packages are created even for artifact aliases, se below in
_Aliases_ section.

For example, if package `foo` contains artifacts
`com.example:foo-artifact` and `bar:baz` then two virtual packages
will be created for package `foo`: one named
`mvn(com.example:foo-artifact)` and the other named `mvn(bar:baz)`.

Craeting virtual packages for Maven artifacts has several advantages.
It makes it easy to search which package provides given artifact, for
example `repoquery --whatprovides 'mvn(bar:baz)'` in the previous
example would return `foo`.  Virtual packages also make it easier to
generate automatic dependencies.
