# Comments start with hash sign
# First part usually consists of metadata such as package name, version, and
# much more
Name:		minimal
Version:	1.0
Release:	1%{?dist}
Summary:	This is a minimal spec file example

License:	GPLv2+
URL:		http://www.fedoraproject.org

# Packages that contain only architecture independent files, such as shell
# scripts or Java programs, should be marked as 'noarch'
BuildArch:  noarch

%description
Very short description since we have nothing to say.

%prep
# section for preparation of sources, applying patches
# or other things which can be done before running the build

%build
# section for compiling and generally assembling the final pieces.

%install
# installation into directory prepared by RPM expressed as %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/minimalistic << EOF
#!/bin/sh
echo This is a minimalistic script
EOF

# List of files that this package installs on the system
%files
%attr(0775,root,root) %{_bindir}/minimalistic


# RPM changelog has prescribed format. To prevent mistakes in format, it is
# advised to use tool such as rpmdev-bumpspec from package rpmdevtools to
# append new changelog entries instead of editing it by hand
%changelog
* Tue Mar 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-1
- This is first version
