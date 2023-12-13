import glob
import os.path
import warnings

def get_component_paths(wildcard="components/**/src/*.vhd"):
    return glob.glob(wildcard)


def get_procedure_paths(wildcard="routines/**/src/*.vhd"):
    return glob.glob(wildcard)


def get_library_paths(wildcard="libs/*"):
    return [d for d in glob.glob(wildcard)
      if os.path.isfile(d + "/Manifest.py")
      or warnings.warn("Library '%s' lacks Manifest.py file" %(d))]
