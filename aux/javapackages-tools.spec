# Don't generate requires on jpackage-utils and java-headless for
# provided pseudo-artifacts: com.sun:tools and sun.jdk:jconsole.
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}/maven-metadata/javapackages-metadata.xml$

# Avoid circular dependency on itself when bootstrapping
%{!?_with_bootstrap: %global bootstrap 0}

%bcond_without tests

%global pkg_name javapackages-tools
%{?scl:%scl_package javapackages-tools}
%if ! 0%{?bootstrap}
%{?sclraw_find_provides_and_requires}
%endif

%if 0%{?fedora}
%global python_prefix python3
%global python_interpreter %{__python3}
%else
%global python_prefix python
%global python_interpreter %{__python2}
%endif


Name:           %{?scl_prefix}%{pkg_name}
Version:        5.0.0
Release:        0.git.%(date +%%Y%%m%%d.%%H%%M%%S)

Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://github.com/fedora-java/javapackages
Source0:        javapackages-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  %{python_prefix}-devel
BuildRequires:  %{python_prefix}-lxml
BuildRequires:  %{python_prefix}-setuptools
BuildRequires:  %{python_prefix}-nose
BuildRequires:  %{python_prefix}-six
BuildRequires:  make
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  scl-utils-build
%if ! 0%{?bootstrap}
BuildRequires:  %{?scl_prefix}javapackages-tools >= 4.0.0
BuildRequires:  %{?scl_prefix}xmvn-resolve >= 3.0.0
%endif

Requires:       coreutils
Requires:       findutils
Requires:       which
Requires:       lua
Requires:       %{?scl_prefix}%{python_prefix}-javapackages = %{version}-%{release}
Requires:       %{python_prefix}

Provides:       %{?scl_prefix}jpackage-utils = %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n %{?scl_prefix}maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}javapackages-local = %{version}-%{release}
%if ! 0%{?bootstrap}
Requires:       %{?scl_prefix}xmvn-minimal >= 3.0.0
Requires:       %{?scl_prefix}xmvn-mojo >= 3.0.0
Requires:       %{?scl_prefix}xmvn-connector-aether >= 3.0.0
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       %{?scl_prefix}mvn(org.apache.maven.plugins:maven-compiler-plugin)
Requires:       %{?scl_prefix}mvn(org.apache.maven.plugins:maven-jar-plugin)
Requires:       %{?scl_prefix}mvn(org.apache.maven.plugins:maven-resources-plugin)
Requires:       %{?scl_prefix}mvn(org.apache.maven.plugins:maven-surefire-plugin)
# Tests based on JUnit are very common and JUnit itself is small.
# Include JUnit provider for Surefire just for convenience.
Requires:       %{?scl_prefix}mvn(org.apache.maven.surefire:surefire-junit4)
# testng is quite common as well
Requires:       %{?scl_prefix}mvn(org.apache.maven.surefire:surefire-testng)
%endif

%description -n %{?scl_prefix}maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%package -n %{?scl_prefix}gradle-local
Summary:        Local mode for Gradle
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}javapackages-local = %{version}-%{release}
Requires:       %{?scl_prefix}gradle >= 2.2.1-2
Requires:       %{?scl_prefix}xmvn-connector-gradle >= 3.0.0

%description -n %{?scl_prefix}gradle-local
This package implements local mode for Gradle, which allows artifact
resolution using XMvn resolver.

%package -n %{?scl_prefix}ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}javapackages-local = %{version}-%{release}
Requires:       %{?scl_prefix}apache-ivy >= 2.3.0-8
Requires:       %{?scl_prefix}xmvn-connector-ivy >= 3.0.0

%description -n %{?scl_prefix}ivy-local
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.

%package -n %{?scl_prefix}%{python_prefix}-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       %{python_prefix}-lxml
Requires:       %{python_prefix}-six
Obsoletes:      %{?scl_prefix}python-javapackages < %{version}-%{release}

%description -n %{?scl_prefix}%{python_prefix}-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n %{?scl_prefix}javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
%if ! 0%{?bootstrap}
Requires:       %{?scl_prefix}xmvn-install >= 3.0.0
Requires:       %{?scl_prefix}xmvn-subst >= 3.0.0
Requires:       %{?scl_prefix}xmvn-resolve >= 3.0.0
%endif
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       java-devel

%description -n %{?scl_prefix}javapackages-local
This package provides non-essential macros and scripts to support Java packaging.

%prep
%setup -q -n %{pkg_name}-%{version}

# Add SCL namespace to generated provides
%{?scl: sed -i '/<groupId>/{h;s|<.*|<namespace>%{scl}</namespace>|;p;g}' etc/javapackages-metadata.xml}

%build
%{?scl:scl enable %{scl} - << "EOF"}
set -e -x
%configure --pyinterpreter=%{python_interpreter}
./build
%{?scl:EOF}

%install
./install

sed -i 's|mvn_build.py|& --xmvn-javadoc|' $(find %{buildroot} -name macros.fjava)
sed -e 's/.[17]$/&.gz/' -e 's/.py$/&*/' -i files-*

%{?scl: sed -i 's:${rpmconfigdir}/macros.d:%{_root_sysconfdir}/rpm:' install}

%if %{with tests}
%check
%{?scl:scl enable %{scl} - << "EOF"}
set -e -x
./check
%{?scl:EOF}
%endif

%files -f files-common

%files -n %{?scl_prefix}javapackages-local -f files-local

%files -n %{?scl_prefix}maven-local -f files-maven

%files -n %{?scl_prefix}gradle-local -f files-gradle

%files -n %{?scl_prefix}ivy-local -f files-ivy

%files -n %{?scl_prefix}%{python_prefix}-javapackages -f files-python
%license LICENSE

%changelog
