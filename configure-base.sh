vars="
scl
scl_root
scl_root_relative

bindir
datadir
localstatedir
mandir
prefix
rundir
sysconfdir
rpmconfigdir

m2home

javaconfdir
javadir
javadocdir
jnidir
jvmcommondatadir
jvmcommonlibdir
jvmcommonsysconfdir
jvmdatadir
jvmdir
jvmlibdir
jvmprivdir
jvmsysconfdir
mavenpomdir
ivyxmldir
pyinterpreter
abrtlibdir
"

vars_re=$(echo $vars | sed 's/ /\\|/g')

eval $(for _; do echo "$_"; done |
    sed -n 's/^--\('"$vars_re"'\)=\(.*\)$/\1="\2"/;T;p')

test -z "${prefix}" && prefix="/usr/local"
test -z "${bindir}" && bindir="${prefix}/bin"
test -z "${datadir}" && datadir="${prefix}/share"
test -z "${localstatedir}" && localstatedir="${prefix}/var"
test -z "${mandir}" && mandir="${datadir}/man"
test -z "${rundir}" && rundir="${localstatedir}/run"
test -z "${sysconfdir}" && sysconfdir="${prefix}/etc"
test -z "${rpmconfigdir}" && rpmconfigdir="${prefix}/lib/rpm"

test -z "${m2home}" && m2home="${datadir}/xmvn"
test -z "${pyinterpreter}" && pyinterpreter=$(which python)
test -z "${abrtlibdir}" && abrtlibdir="${prefix}/lib/abrt-java-connector"

eval $(sed -n 's/^%_\('"$vars_re"'\)\ *\(.*\)$/\1="\2"/;T;s/%{_\(.*}\)/${\1/;p' macros.d/macros.jpackage)

test -z "${scl_root_relative}" -a -n "${scl_root}" && scl_root_relative=$(sed "s:^/*::" <<<"${scl_root}")
return 0
