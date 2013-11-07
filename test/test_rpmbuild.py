import os
import re
import subprocess
import shutil

from textwrap import dedent

from test_common import DIRPATH

class Package(object):
    """Represents single RPM package that should be built.

    It creates a temporary specfile that is used to build the package using
    rpmbuild.  Every output goes to directory 'rpmbuild' (will be created) in
    current working directory.  RPM macros in javapackages/etc are processed to
    override default lookup for our srcipts in order to test the current
    version and not the system-wide javapackages-tools

    """
    def __init__(self, name):
        self.__name = name
        self.__sources = {}
        self.__prep = ''
        self.__build = ''
        self.buildpath = os.path.join('rpmbuild', 'BUILD', name + '-1')
        self.__env = dict(os.environ)
        self.__env['HOME'] = os.getcwd()
        self.__env['PYTHONPATH'] = os.path.join(DIRPATH, '..', 'python')
        self.__env['PATH'] = '{mock}:{path}'.format(mock=DIRPATH,
                                            path=self.__env['PATH'])

    def add_source(self, sourcepath, newname=None):
        """Add source file to a package

        File will be copied into 'rpmbuild/SOURCES' and 'rpmbuild/BUILD' by
        default. Path can be absolute or relative to test directory.

        Keyword arguments:
        newname -- name for source file. If None, sourcepath's basename will be
        used.

        """
        if not os.path.isabs(sourcepath):
            sourcepath = os.path.join(DIRPATH, sourcepath)
        if not newname:
            newname = os.path.basename(sourcepath)
        self.__sources[sourcepath] = newname

    def append_to_prep(self, to_append):
        """Appends given string to %prep section of spec."""
        self.__prep += to_append + '\n'

    def append_to_build(self, to_append):
        """Appends given string to %build section of spec."""
        self.__build += to_append + '\n'

    def run_prep(self):
        """Runs rpmbuild -bp (doing only prep phase) with current settings."""
        self.__prepare_all()
        return self.__invoke_rpmbuild(['-bp'])

    def run_build(self):
        """Runs rpmbuild -bb (stop after build phase) with current settings."""
        self.__prepare_all()
        return self.__invoke_rpmbuild(['-bb'])

    def __invoke_rpmbuild(self, args):
        outfile = open("tmpout", 'w')
        errfile = open("tmperr", 'w')
        topdir = '--define=_topdir {cwd}/rpmbuild'.format(cwd=os.getcwd())
        proc = subprocess.Popen(['rpmbuild', topdir,
                                 os.path.join('rpmbuild', 'SPECS',
                                              self.__name + '.spec')]
                                + args, shell=False, env=self.__env,
                                stdout=outfile, stderr=errfile)
        ret = proc.wait()
        outfile = open("tmpout", 'r+')
        errfile = open("tmperr", 'r+')
        out = outfile.read()
        err = errfile.read()
        os.remove('tmpout')
        os.remove('tmperr')
        return (out, err, ret)

    def set_env(self, name, value):
        self.__env[name] = value

    def __prepare_all(self):
        try:
            os.mkdir('rpmbuild')
            os.mkdir('rpmbuild/SOURCES')
            os.mkdir('rpmbuild/SPECS')
            os.mkdir('rpmbuild/RPMS')
            os.mkdir('rpmbuild/SRPMS')
            os.mkdir('rpmbuild/BUILD')
            os.mkdir('rpmbuild/BUILDROOT')
        except OSError:
            pass
        _prepare_macros()
        self.__prepare_spec()
        try:
            self.__prepare_sources()
        except IOError:
            pass

    def __prepare_spec(self):
        header = dedent("""\
        Name:    {name}
        Version:    1
        Release:    1%{{?dist}}
        Summary:    test
        License:    GPL
        URL:        www.example.com
        """.format(name=self.__name))
        for index, filename in enumerate(self.__sources.values() or []):
            header += 'Source{index}: {filename}\n'.format(filename=filename,
                    index=index)

        header += dedent("""\
        %description
        This is just a test.
        """)

        prep_section = dedent("""\

        %prep
        mkdir %{name}-%{version}
        cd %{name}-%{version}
        """)
        for i in range(len(self.__sources)):
            prep_section += 'cp -p %SOURCE{index} .\n'.format(index=i)
        prep_section += self.__prep

        build_section = dedent("""\

        %build
        cd %{name}-%{version}
        """)
        build_section += self.__build

        specpath = os.path.join('rpmbuild', 'SPECS', self.__name + '.spec')
        with open(specpath, 'w') as specfile:
            specfile.write(header)
            specfile.write(prep_section)
            specfile.write(build_section)

    def __prepare_sources(self):
        destpath = os.path.join('rpmbuild', 'SOURCES')
        for sourcepath, targetname in self.__sources.iteritems():
            shutil.copy(sourcepath, os.path.join(destpath, targetname))

def _prepare_macros():
    etcpath = os.path.join(DIRPATH, '..', 'etc')
    java_utils = os.path.abspath(os.path.join(DIRPATH, '..', 'java-utils'))

    with open('.rpmmacros', 'w') as rpmmacros:
        for filepath in os.listdir(etcpath):
            if filepath.startswith('macros'):
                with open(os.path.join(etcpath, filepath), 'r') as macrofile:
                    for line in macrofile:
                        if '/usr/share/java-utils' in line:
                            rpmmacros.write(re.sub(r'/usr/share/java-utils',
                                    java_utils, line))
                        elif '%{javadir}-utils' in line:
                            rpmmacros.write(re.sub(r'%\{javadir\}-utils',
                                    java_utils, line))
                        else:
                            rpmmacros.write(line)
