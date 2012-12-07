#! /usr/bin/python
''' Build file that compiles all the needed resources'''
import os.path
import os
import sys
import datetime
from fabricate import *
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
import optparse

ui_sources = ['src/ui_datatimerpicker', 'src/ui_listmodules',
              'src/syncing/ui_sync', 'src/ui_listfeatures', 'src/ui_errorlist',
              'src/ui_helpviewer']

doc_sources = ['docs/README', 'docs/ClientSetup', 'docs/UserGuide']

path = os.path.dirname(__file__)

APPNAME = "QMap"

curpath = os.path.dirname(os.path.abspath(__file__))
srcopyFilesath = os.path.join(curpath, "src")
buildpath = os.path.join(curpath, "build", APPNAME)
deploypath = os.path.join(curpath, "build", APPNAME, APPNAME.lower())
targetspath = os.path.join(curpath, 'targets.ini')
bootpath = os.path.join(curpath, "loader_src")
dotnetpath = os.path.join(curpath, "dotnet")

flags = '--update -rvp'.split()

iswindows = os.name == 'nt'

if iswindows:
    # Add the path to MSBuild to PATH so that subprocess can find it.
    env = os.environ.copy()
    env['PATH'] += ";c:\\WINDOWS\\Microsoft.NET\Framework\\v3.5"

def build():
    """
    Build the project.
    """
    build_plugin()


def compileplugin():
    print " - building UI files..."
    for source in ui_sources:
        pyuic = 'pyuic4'
        if iswindows:
            pyuic += '.bat'

        run(pyuic, '-o', source + '.py', source + '.ui')

    print " - building resource files..."
    run('pyrcc4', '-o', 'src/resources_rc.py', 'src/resources.qrc')
    run('pyrcc4', '-o', 'src/syncing/resources_rc.py', 'src/syncing/resources.qrc')

    if iswindows and main.options.with_mssyncing == True:
        print " - building syncing tools..."
        run('MSBuild', '/property:Configuration=Release', '/verbosity:m', \
            'dotnet/libsyncing/libsyncing.csproj', shell=True, env=env)
        run('MSBuild', '/property:Configuration=Release', '/verbosity:m', \
            'dotnet/provisioner/provisioner.csproj', \
            shell=True, env=env)
        run('MSBuild', '/property:Configuration=Release', '/verbosity:m', \
            'dotnet/syncer/syncer.csproj', \
            shell=True, env=env)

    print " - building docs..."
    docs()


def docs():
    if main.options.with_docs == True:
		print "Generating docs"
		for doc in doc_sources:
			run('python', 'docs/rst2html.py', doc + '.rst', doc + '.html')


def clean():
    autoclean()
    msg = shell('rm', '-r', buildpath)


def getVersion():
    """
        Returns the version number for the plugin
    """
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    try:
		commit = shell('git', 'log', '-1', '--pretty=%h').strip()
    except WindowsError:
		commit = ""
    return "{0}.{1}.{2}.{3}".format(year, month, day, commit)


def test():
    """
        Run the tests in the project
    """
    print "Running tests..."
    import unittest
    from src import tests
    loader = unittest.TestLoader()
    allsuite = loader.loadTestsFromModule(tests)
    result = unittest.TextTestRunner().run(allsuite)
    return result.wasSuccessful()

def build_plugin():
    """
        Builds the QGIS plugin and sends the output into the build directory.
    """
    print "Deploy started"
    print "Building..."
    compileplugin()
    if main.options.with_tests == True:
        passed = test()
        if not passed:
            print "Tests Failed!!"
            sys.exit()

    # Copy all the files to the ouput directory
    print "Copying new files..."

    mkdir(deploypath)
    copyFiles(srcopyFilesath,deploypath)
    copyFiles(bootpath,buildpath)

    if iswindows and main.options.with_mssyncing == True:
        mssyncpath = os.path.join(dotnetpath, "bin")
        lib = os.path.join(mssyncpath, "libsyncing.dll")
        bin = os.path.join(mssyncpath, "syncer.exe")
        destmssyncpath = os.path.join(deploypath,"syncing")
        copyFolder(lib, destmssyncpath)
        copyFolder(bin, destmssyncpath)
    # Replace version numbers
    version = getVersion()
    command = 's/version=0.1/version=%s/ "%s"' % (version, os.path.join(deploypath, 'metadata.txt'))
    #run("sed", command)

    print "Local build into {0}".format(deploypath)

def copyFiles(src, dest):
    src = os.path.join(src,'*')
    if iswindows:
        src = src.replace('\\','/')
        dest = dest.replace('\\','/')
    msg = shell('cp', flags, src , dest, shell=True, silent=False)

def copyFolder(src, dest):
    if iswindows:
        src = src.replace('\\','/')
        dest = dest.replace('\\','/')
    msg = shell('cp', flags, src, dest, shell=True, silent=False)

def mkdir(path):
    if iswindows:
        path = path.replace('\\','/')
    msg = shell('mkdir', '-p', path, silent=False)

def deploy():
    targetname = main.options.target
    if targetname is None:
        print "No target name given depolying All target"
        targetname = 'All'

    config = ConfigParser()
    config.read(targetspath)

    try:
        config.get(targetname, 'client').split(',')
    except NoSectionError as ex:
        print "No client in targets.ini defined as %s" % targetname
        return

    build_plugin()
    deploy_target(targetname, config)


def deploy_to(target, config):
    print "Remote depolying to %s" % target

    projects = config['projects']
    forms = config['forms']
    clientpath = os.path.normpath(config['client'])

    print "Deploying application to %s" % config['client']
    clientpath = os.path.join(clientpath, APPNAME)
    mkdir(clientpath)
    copyFiles(buildpath,clientpath)

    projecthome = os.path.join(curpath, 'project-manager', 'projects')
    clientpojecthome = os.path.join(clientpath, APPNAME.lower(), 'projects')

    print projecthome

    formpath = os.path.join(curpath, 'project-manager', 'entry_forms')
    clientformpath = os.path.join(clientpath, APPNAME.lower(), 'entry_forms')

    print formpath

    mkdir(clientpojecthome)
    mkdir(clientformpath)

    if 'All' in projects:
        print "Loading all projects"
        copyFiles(projecthome, clientpojecthome )
    else:
        for project in projects:
            if project and project[-4:] == ".qgs":
                print "Loading project %s" % project
                path = os.path.join(projecthome, project)
                newpath = os.path.join(clientpojecthome, project)
                copyFolder(path, newpath)
                icon = project[:-4] + ".png"
                path = os.path.join(projecthome, icon)
                newpath = os.path.join(clientpojecthome, icon)
                copyFolder(path, newpath)

    if 'All' in forms:
        print "Loading all forms"
        copyFiles(formpath, clientformpath )
    else:
        for form in forms:
            if form:
                print "Loading form %s" % form
                path = os.path.join(formpath, form)
                newpath = os.path.join(clientformpath, form)
                if os.path.exists(newpath):
                    copyFiles(path, newpath )
                else:
                    copyFolder(path, newpath)

    print "Remote depoly compelete"


def deploy_target(targetname, config):
    targets = {}
    try:
        clients = config.get(targetname, 'client').split(',')
        for client in clients:
            client = client.strip()
            if client == targetname:
                print "Can't include a section as a deploy target of itself"
                continue

            if client in config.sections():
                deploy_target(client, config)
            else:
                print 'Client -> %s' % client
                projects = config.get(targetname, 'projects').split(',')
                forms = config.get(targetname, 'forms').split(',')
                targets[targetname] = {'client': client, 'projects': projects, \
                                 'forms': forms}

            for target, items in targets.iteritems():
                deploy_to(target, items)

    except NoSectionError as ex:
        print ex.message
    except NoOptionError as ex:
        print ex.message

if __name__ == "__main__":
    options = [
        optparse.make_option('-o', '--target', dest='target', help='Target to deploy'),
        optparse.make_option('--with-tests', action='store', help='Enable tests!', \
                             default=True),
        optparse.make_option('--with-mssyncing', action='store', help='Use MS SQL Syncing!', \
                             default=True),
		optparse.make_option('--with-docs', action='store', help='Build docs', \
                             default=True)
    ]

    main(extra_options=options)
