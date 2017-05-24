# Don't generate requires on jpackage-utils and java-headless for
# provided pseudo-artifacts: com.sun:tools and sun.jdk:jconsole.
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}/maven-metadata/javapackages-metadata.xml$

# %{scl}-runtime requires us, not the other way
%{?scl:%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{scl}-runtime$}

%bcond_without gradle
%bcond_without tests

%global pkg_name javapackages-tools
%{?scl:%scl_package javapackages-tools}

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

BuildRequires:  coreutils
BuildRequires:  which
BuildRequires:  make
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  scl-utils-build
BuildRequires:  %{python_prefix}-devel
BuildRequires:  %{python_prefix}-lxml
BuildRequires:  %{python_prefix}-setuptools
BuildRequires:  %{python_prefix}-nose
BuildRequires:  %{python_prefix}-six

Requires:       coreutils
Requires:       findutils
Requires:       which

Obsoletes:      %{?scl_prefix}eclipse-filesystem < 2
Provides:       %{?scl_prefix}eclipse-filesystem = %{version}-%{release}
Provides:       %{?scl_prefix}jpackage-utils = %{version}-%{release}
# These could be generated automatically, but then we would need to
# depend on javapackages-local for dependency generator.
Provides:       %{?scl_prefix}mvn(com.sun:tools) = SYSTEM
Provides:       %{?scl_prefix}mvn(sun.jdk:jconsole) = SYSTEM

%description
This package provides macros and scripts to support Java packaging.

%package -n %{?scl_prefix}maven-local
Summary:        Macros and scripts for Maven packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}javapackages-local = %{version}-%{release}
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
# Include JUnit and JUnit provider for Surefire just for convenience.
Requires:       %{?scl_prefix}mvn(junit:junit)
Requires:       %{?scl_prefix}mvn(org.apache.maven.surefire:surefire-junit4)
# testng is quite common as well
Requires:       %{?scl_prefix}mvn(org.apache.maven.surefire:surefire-testng)

%description -n %{?scl_prefix}maven-local
This package provides macros and scripts to support packaging Maven artifacts.

%if %{with gradle}
%package -n %{?scl_prefix}gradle-local
Summary:        Local mode for Gradle
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}javapackages-local = %{version}-%{release}
Requires:       %{?scl_prefix}gradle >= 2.2.1-2
Requires:       %{?scl_prefix}xmvn-connector-gradle >= 3.0.0

%description -n %{?scl_prefix}gradle-local
This package implements local mode for Gradle, which allows artifact
resolution using XMvn resolver.
%endif

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
Requires:       %{?scl_prefix}xmvn-install >= 3.0.0
Requires:       %{?scl_prefix}xmvn-subst >= 3.0.0
Requires:       %{?scl_prefix}xmvn-resolve >= 3.0.0
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       java-devel
Requires:       %{?scl_prefix}%{python_prefix}-javapackages = %{version}-%{release}
Requires:       %{python_prefix}

%description -n %{?scl_prefix}javapackages-local
This package provides non-essential macros and scripts to support Java packaging.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
%configure --pyinterpreter=%{python_interpreter} %{?scl:--rpmconfigdir=%{_root_prefix}/lib/rpm --scl=%{scl} --scl_root=%{_scl_root}}
./build

%install
./install

sed -i 's|mvn_build.py|& --xmvn-javadoc|' $(find %{buildroot} -name macros.fjava)
sed -e 's/.[17]$/&.gz/' -e 's/.py$/&*/' -i files-*

%{?scl:
  mv %{buildroot}%{_root_prefix}/lib/rpm/macros.d/macros{,.%{scl}}.fjava
  mv %{buildroot}%{_root_prefix}/lib/rpm/macros.d/macros{,.%{scl}}.jpackage
  mv %{buildroot}%{_root_prefix}/lib/rpm/maven{,.%{scl}}.req
  mv %{buildroot}%{_root_prefix}/lib/rpm/maven{,.%{scl}}.prov
  mv %{buildroot}%{_root_prefix}/lib/rpm/osgi{,.%{scl}}.req
  mv %{buildroot}%{_root_prefix}/lib/rpm/osgi{,.%{scl}}.prov
  mv %{buildroot}%{_root_prefix}/lib/rpm/javadoc{,.%{scl}}.req
  mv %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/maven{,.%{scl}}.attr
  mv %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/osgi{,.%{scl}}.attr
  mv %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/javadoc{,.%{scl}}.attr
  sed -i 's:\(macros\.\)\(fjava\|jpackage\):\1%{scl}.\2:' files-*
  sed -i 's:\(maven\|osgi\|javadoc\)\.\(req\|prov\|attr\):\1.%{scl}.\2:' \
      files-* %{buildroot}%{_root_prefix}/lib/rpm/*{.req,.prov,fileattrs/*}
}

%if %{without gradle}
rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%endif

%if %{with tests}
%check
./check
%endif

%files -f files-common

%files -n %{?scl_prefix}javapackages-local -f files-local

%files -n %{?scl_prefix}maven-local

%if %{with gradle}
%files -n %{?scl_prefix}gradle-local -f files-gradle
%endif

%files -n %{?scl_prefix}ivy-local -f files-ivy

%files -n %{?scl_prefix}%{python_prefix}-javapackages -f files-python
%license LICENSE

%changelog
