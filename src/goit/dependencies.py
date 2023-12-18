import glob
import os.path
import os.link
import tempfile
import warnings


def get_component_paths(wildcard="components/**/src/*.vhd"):
    """Returns a list of source files (components) corresponding to the wildcard
    (default: 'components/**/src/*.vhd')"""
    return glob.glob(wildcard)


def get_procedure_paths(wildcard="routines/**/src/*.vhd"):
    """Returns a list of source files (routines) corresponding to the wildcard
    (default: 'routines/**/src/*.vhd')"""
    return glob.glob(wildcard)


def get_library_paths(wildcard="libs/*"):
    """Returns a list of directories (libraries) corresponding to the wildcard
    (default: 'libs/*')"""
    return [d for d in glob.glob(wildcard)
      if os.path.isfile(d + "/Manifest.py")
      or warnings.warn("Library '%s' lacks Manifest.py file" %(d))]


def get_dependencies_hdlmake(path_top, path_repo):
    # TODO: retreive relative file paths for source files and tests

    # create temporary file
    fd = tempfile.NamedTemporaryFile(mode='w', dir=path)

    # link temporary file 'Manifest.py'
    os.link(fd.name, "Manifest.py")

    # TODO: construct 'Manifest.py'

    # aggregate dependencies using hdlmake
    dependencies = subprocess.check_output("hdlmake list-json", shell=True)

    # unlink 'Manifest.py'
    os.unlink("Manifest.py")

    # close temporary file
    fd.close()

    return dependencies


def get_dependencies(path_top, path_repo):
    return get_dependencies_hdlmake(path_top, path_repo)
