import io
import os
import re
import sys
import subprocess
import shutil

from textwrap import dedent

DIRPATH = os.path.dirname(os.path.realpath(__file__))

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
        self.__sources = []
        self.__begin = ''
        self.__prep = ''
        self.__build = ''
        self.__install = ''
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
        self.__sources.append((sourcepath, newname))

    def prepend(self, to_prepend):
        """Prepends given string to spec file"""
        self.__begin += to_prepend

    def append_to_prep(self, to_append):
        """Appends given string to %prep section of spec."""
        self.__prep += to_append + '\n'

    def append_to_build(self, to_append):
        """Appends given string to %build section of spec."""
        self.__build += to_append + '\n'

    def append_to_install(self, to_append):
        """Appends given string to %install section of spec."""
        self.__install += to_append + '\n'

    def run_prep(self, args=None):
        """Runs rpmbuild -bp (doing only prep phase) with current settings."""
        self.__prepare_all()
        return self.__invoke_rpmbuild(['-bp'] + (args or []))

    def run_build(self, args=None):
        """Runs rpmbuild -bc (stop after build phase) with current settings."""
        self.__prepare_all()
        return self.__invoke_rpmbuild(['-bc'] + (args or []))

    def run_install(self, args=None):
        """Runs rpmbuild -bi (stop after install) with current settings."""
        self.__prepare_all()
        return self.__invoke_rpmbuild(['-bi'] + (args or []))

    def __invoke_rpmbuild(self, args):
        outfile = open("tmpout", 'w')
        errfile = open("tmperr", 'w')
        topdir = '--define=_topdir {cwd}/rpmbuild'.format(cwd=os.getcwd())
        scl_undef = '--eval=%undefine scl'
        proc = subprocess.Popen(['rpmbuild', topdir, scl_undef,
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
        self.__prepare_sources()

    def __prepare_spec(self):
        header = self.__begin + dedent("""
        Name:    {name}
        Version:    1
        Release:    1%{{?dist}}
        Summary:    test
        License:    GPL
        URL:        www.example.com
        """.format(name=self.__name))
        for index, (_, filename) in enumerate(self.__sources):
            filename = os.path.basename(filename)
            header += 'Source{index}: {filename}{index}\n'.format(filename=filename,
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
        for index, (_, filename) in enumerate(self.__sources):
            directory = os.path.dirname(filename)
            prep_section += 'mkdir -p ./{d}\n'.format(d=directory)
            prep_section += 'cp -p %SOURCE{index} ./{d}/{f}\n'.format(index=index,
                d=directory, f=os.path.basename(filename))

        prep_section += self.__prep

        build_section = dedent("""\

        %build
        cd %{name}-%{version}
        """)
        build_section += self.__build

        install_section = dedent("""\

        %install
        """)
        install_section += self.__install

        specpath = os.path.join('rpmbuild', 'SPECS', self.__name + '.spec')
        with open(specpath, 'w') as specfile:
            specfile.write(header)
            specfile.write(prep_section)
            specfile.write(build_section)
            specfile.write(install_section)

    def __prepare_sources(self):
        destpath = os.path.join('rpmbuild', 'SOURCES')
        for index, (sourcepath, targetname) in enumerate(self.__sources):
            target = os.path.join(destpath, os.path.basename(targetname))
            shutil.copy(sourcepath, '{0}{1}'.format(target, index))


def _prepare_macros():
    macropath = os.path.join(DIRPATH, '..', 'macros.d')
    java_utils = os.path.abspath(os.path.join(DIRPATH, '..', 'java-utils'))

    with io.open('.rpmmacros', 'wt', encoding='utf-8') as rpmmacros:
        for filepath in os.listdir(macropath):
            if filepath.startswith('macros'):
                with io.open(os.path.join(macropath, filepath), encoding='utf-8') as macrofile:
                    for line in macrofile.readlines():
                        if '/usr/share/java-utils' in line:
                            line = re.sub(r'/usr/share/java-utils',
                                          java_utils, line)
                        if '%{javadir}-utils' in line:
                            line = re.sub(r'%\{javadir\}-utils',
                                          java_utils, line)
                        if '%{pyinterpreter}' in line:
                            line = re.sub(r'%\{pyinterpreter\}',
                                          sys.executable.split('/')[-1], line)
                        rpmmacros.write(line)
