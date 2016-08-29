# Don't generate requires on jpackage-utils and java-headless for
# provided pseudo-artifacts: com.sun:tools and sun.jdk:jconsole.
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}/maven-metadata/javapackages-metadata.xml$

# Avoid circular dependency on itself when bootstrapping
%{!?_with_bootstrap: %global bootstrap 0}

%bcond_without tests

Name:           javapackages-tools
Version:        5.0.0
Release:        0.git.%(date +%%Y%%m%%d.%%H%%M%%S)

Summary:        Macros and scripts for Java packaging support

License:        BSD
URL:            https://github.com/fedora-java/javapackages
Source0:        javapackages-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-six
BuildRequires:  make
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  scl-utils-build
BuildRequires:  dia
%if ! 0%{?bootstrap}
BuildRequires:  javapackages-tools >= 4.0.0
BuildRequires:  xmvn-resolve >= 2
%endif

Requires:       coreutils
Requires:       findutils
Requires:       lua
Requires:       python3-javapackages = %{version}-%{release}
Requires:       python3

Provides:       jpackage-utils = %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       xmvn-minimal >= 2
Requires:       xmvn-mojo >= 2
Requires:       xmvn-connector-aether >= 2
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       maven-compiler-plugin
Requires:       maven-jar-plugin
Requires:       maven-resources-plugin
Requires:       maven-surefire-plugin
# Tests based on JUnit are very common and JUnit itself is small.
# Include JUnit provider for Surefire just for convenience.
Requires:       maven-surefire-provider-junit
# testng is quite common as well
Requires:       maven-surefire-provider-testng

%description -n maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%package -n gradle-local
Summary:        Local mode for Gradle
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       gradle >= 2.2.1-2
Requires:       xmvn-connector-gradle >= 2

%description -n gradle-local
This package implements local mode for Gradle, which allows artifact
resolution using XMvn resolver.

%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       xmvn-connector-ivy >= 2

%description -n ivy-local
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.

%package -n python3-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       python3-lxml
Requires:       python3-six
Obsoletes:      python-javapackages < %{version}-%{release}

%description -n python3-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       xmvn-install >= 2
Requires:       xmvn-subst >= 2
Requires:       xmvn-resolve >= 2
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       java-devel

%description -n javapackages-local
This package provides non-essential macros and scripts to support Java packaging.

%prep
%setup -q

sed -i '/fedora-review/d' install

%build
%configure --pyinterpreter=%{__python3}
./build

%install
./install
sed -i 's|mvn_build.py|& --xmvn-javadoc|' %{buildroot}/usr/lib/rpm/macros.d/macros.fjava
sed -e 's/.[17]$/&.gz/' -e 's/.py$/&*/' -i files-*

pushd python
  %{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd

%if %{with tests}
%check
./check
%endif

%files -f files-common

%files -n javapackages-local -f files-local

%files -n maven-local -f files-maven

%files -n gradle-local -f files-gradle

%files -n ivy-local -f files-ivy

%files -n python3-javapackages
%license LICENSE
%{python3_sitelib}/javapackages*

%changelog
