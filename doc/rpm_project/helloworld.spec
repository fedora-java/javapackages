# Comments start with hash sign. Caution: macros in comments are still
# expanded, which can lead to unexpected results. To stop macro from expanding,
# double its percent sign (e.g. %%mvn_install)

# First part usually consists of metadata such as package name, version, and
# much more
Name:		helloworld
Version:	1.0
Release:	1%{?dist}
Summary:	This is a minimal spec file example

License:	GPLv2+
# Homepage URL of the project
URL:		http://www.fedoraproject.org

# Our source archive. %{name} expands to 'helloworld' so the resulting
# tarball name would be 'helloworld.tar.gz'.
Source0:    %{name}.tar.gz

# Packages that contain only architecture independent files, such as shell
# scripts or regular Java programs (not JNI libraries), should be marked as 'noarch'
BuildArch:  noarch

# Project's build time dependency. We don't really need JUnit, it just
# serves as and example
BuildRequires: junit

%description
Very short description since we have nothing to say.

%prep
# section for preparation of sources, applying patches
# or other things which can be done before running the build
# The macro setup is used to unpack sources
%setup -q

%build
# Section for compiling and generally assembling the final pieces.
# Our Makefile builds the project JAR file
make {?_smp_flags}

%install
# Installation into directory prepared by RPM expressed as %{buildroot}
install -p -m 644 helloworld.jar %{buildroot}%{_javadir}/helloworld.jar

# We use macro %jpackage_script to generate wrapper script for our JAR
# Will be explained in later sections
%jpackage_script org.fedoraproject.helloworld.HelloWorld "" "" %{name} helloworld true

# List of files that this package installs on the system
%files
%{_javadir}/helloworld.jar
%{_bindir}/helloworld

%changelog
* Tue Mar 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-1
- This is first version
