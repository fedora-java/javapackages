How to report bugs
==================

When reporting bugs related to failing Java builds, **please** include
at least the following information:

1. build log with **debugging information** enabled

Debugging output provides valuable information which often is
essential to discover the real cause of the build failure

2. versions of relevant packages

Quite often it's necessary to chech versions of packages involved in
the bug.  There may be multiple reasons for doing that.  One of them
is ruling out possible causes basing on changes madein each version.
Ideally a list of all installed packages with their versions (`rpm
-qa`) should be included.

3. exact steps how to reliably reproduce the bug

Reproducer such as "try to build package foo" is not good enough
(which version of package? in what environment? on which architecture?
using what Java version? etc.).  If the reproducer is available in
public git repository it's usually better to provide git URL and
commit hash then attaching the reproducer to the bugzilla.

Build logs

It's worth noting that providing a Koji task ID of failed SCM build
with debugging enabled is often enough to cover all the above points.
Build environment is known, `build.log` covers point 1, `root.log`
provides version of all installed packages.  Even if build logs
expired the task metadata has enough information (like git URL, commit
hash etc.) to reproduce the build failure.
