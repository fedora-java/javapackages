%if 0%{?fedora}
%bcond_without ivy
%else
%bcond_with ivy
%endif

%global python_prefix python3
%global python_interpreter %{?__python3}%{!?__python3:dummy}

%global maven_home %{_usr}/share/xmvn

Name:           javapackages-tools
Version:        [...]
Release:        %autorelease
Summary:        Macros and scripts for Java packaging support
License:        BSD-3-Clause
URL:            https://github.com/fedora-java/javapackages
BuildArch:      noarch

Source:         https://github.com/fedora-java/javapackages/archive/%{version}.tar.gz

Source21:       toolchains-openjdk21.xml

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  rubygem-asciidoctor
BuildRequires:  %{python_prefix}-devel
BuildRequires:  %{python_prefix}-lxml
BuildRequires:  %{python_prefix}-setuptools
BuildRequires:  %{python_prefix}-pytest

Requires:       javapackages-filesystem = %{version}-%{release}
Requires:       coreutils
Requires:       findutils

Provides:       jpackage-utils = %{version}-%{release}

%description
This package provides macros and scripts to support Java packaging.

%package -n javapackages-filesystem
Summary:        Java packages filesystem layout
Provides:       eclipse-filesystem = %{version}-%{release}

%description -n javapackages-filesystem
This package provides some basic directories into which Java packages
install their content.

%package -n maven-local-openjdk21
Summary:        Macros and scripts for Maven packaging support
RemovePathPostfixes: -openjdk21
Requires:       java-21-openjdk-devel
Provides:       maven-local = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local-openjdk21 = %{version}-%{release}
Requires:       xmvn-minimal
Requires:       mvn(org.fedoraproject.xmvn:xmvn-mojo)
# Common Maven plugins required by almost every build. It wouldn't make
# sense to explicitly require them in every package built with Maven.
Requires:       mvn(org.apache.maven.plugins:maven-compiler-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-jar-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-resources-plugin)
Requires:       mvn(org.apache.maven.plugins:maven-surefire-plugin)
# Remove in Fedora 45
Obsoletes:      maven-local < 6.3.0
Obsoletes:      maven-local-openjdk8 < 6.2.0-29
Obsoletes:      maven-local-openjdk11 < 6.2.0-29
Obsoletes:      maven-local-openjdk17 < 6.2.0-29

%description -n maven-local-openjdk21
This package provides macros and scripts to support packaging Maven artifacts.

%if %{with ivy}
%package -n ivy-local
Summary:        Local mode for Apache Ivy
Requires:       %{name} = %{version}-%{release}
Requires:       javapackages-local = %{version}-%{release}
Requires:       apache-ivy >= 2.3.0-8
Requires:       xmvn-connector-ivy

%description -n ivy-local
This package implements local mode for Apache Ivy, which allows
artifact resolution using XMvn resolver.
%endif

%package -n %{python_prefix}-javapackages
Summary:        Module for handling various files for Java packaging
Requires:       %{python_prefix}-lxml

%description -n %{python_prefix}-javapackages
Module for handling, querying and manipulating of various files for Java
packaging in Linux distributions

%package -n javapackages-local-openjdk21
Summary:        Non-essential macros and scripts for Java packaging support
Obsoletes:      javapackages-local < 6.3.0
Provides:       javapackages-local = %{version}-%{release}
Requires:       javapackages-common = %{version}-%{release}
Requires:       xmvn-tools
# Java build systems don't have hard requirement on java-devel, so it should be there
Requires:       java-21-openjdk-devel
Requires:       xmvn-generator
Obsoletes:      javapackages-generators < 6.3.0

%description -n javapackages-local-openjdk21
This package provides non-essential macros and scripts to support Java packaging.

%package -n javapackages-common
Summary:        Non-essential macros and scripts for Java packaging support
Requires:       %{name} = %{version}-%{release}
Requires:       %{python_prefix}-javapackages = %{version}-%{release}
Requires:       %{python_interpreter}

%description -n javapackages-common
This package provides non-essential, but commonly used macros and
scripts to support Java packaging.

%package -n javapackages-compat
Summary:        Previously deprecated macros and scripts for Java packaging support
Requires:       javapackages-local = %{version}-%{release}

%description -n javapackages-compat
This package provides previously deprecated macros and scripts to
support Java packaging as well as some additions to them.

%prep
%autosetup -p1 -C

%build
%configure --pyinterpreter=%{python_interpreter} \
    --rpmmacrodir=%{_rpmmacrodir} --rpmconfigdir=%{_rpmconfigdir} \
    --m2home=%{maven_home} \
    --jvm=openjdk21=%{_jvmdir}/jre-21-openjdk
./build

%install
./install

sed -e 's/.[17]$/&*/' -i files-*

rm -rf %{buildroot}%{_bindir}/gradle-local
rm -rf %{buildroot}%{_datadir}/gradle-local
rm -rf %{buildroot}%{_mandir}/man7/gradle_build.7
%if %{without ivy}
rm -rf %{buildroot}%{_sysconfdir}/ivy
rm -rf %{buildroot}%{_sysconfdir}/ant.d
%endif

mkdir -p %{buildroot}%{maven_home}/conf/
cp -p %{SOURCE21} %{buildroot}%{maven_home}/conf/toolchains.xml-openjdk21

%if 0%{?flatpak}
# make both /app (runtime deps) and /usr (build-only deps) builds discoverable
sed -e '/^JAVA_LIBDIR=/s|$|:/usr/share/java|' \
    -e '/^JNI_LIBDIR=/s|$|:/usr/lib/java|' \
    -i %{buildroot}%{_sysconfdir}/java/java.conf
%if %{with ivy}
# fix ivy paths
mkdir -p %{buildroot}/etc
mv %{buildroot}%{_sysconfdir}/{ant.d,ivy} %{buildroot}/etc/
sed -i -e 's|%{_sysconfdir}|/etc|' files-ivy
%endif
# /usr path is hard-coded in ant and xmvn
mkdir -p %{buildroot}%{_usr}/{bin,share}
ln -s %{_bindir}/build-classpath %{buildroot}%{_usr}/bin/build-classpath
ln -s %{_datadir}/java-utils %{buildroot}%{_usr}/share/java-utils
%endif

%check
./check

%files -f files-tools
%if 0%{?flatpak}
%{_usr}/bin/build-classpath
%{_usr}/share/java-utils
%endif

%files -n javapackages-filesystem -f files-filesystem

%files -n javapackages-common -f files-common

%files -n javapackages-compat -f files-compat

%files -n javapackages-local-openjdk21 -f files-local-openjdk21

%files -n maven-local-openjdk21
%dir %{maven_home}/conf
%{maven_home}/conf/toolchains.xml-openjdk21

%if %{with ivy}
%files -n ivy-local -f files-ivy
%endif

%files -n %{python_prefix}-javapackages -f files-python
%license LICENSE

%changelog
%autochangelog
