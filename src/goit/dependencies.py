import glob
import os
import json
import tempfile
import warnings
import subprocess


def get_component_paths(wildcard="components/**/src/*.vhd"):
  """Returns a list of source files (components) corresponding to the wildcard
  (default: 'components/**/src/*.vhd')"""
  return glob.glob(wildcard)


def get_procedure_paths(wildcard="routines/**/src/*.vhd"):
  """Returns a list of source files (routines) corresponding to the wildcard
  (default: 'routines/**/src/*.vhd')"""
  return glob.glob(wildcard)


def get_library_paths(wildcard="libs/*"):
  '''Returns a list of directories (libraries) corresponding to the wildcard
  (default: "libs/*")'''
  return [d for d in glob.glob(wildcard)
    if os.path.isfile(d + "/Manifest.py")
    or warnings.warn("Library '%s' lacks Manifest.py file" %(d))]


def get_dependencies_hdlmake(path_repo, path_target, sim_tool='ghdl', sim_opts='-2008'):
  '''
  Retreives dependencies using hdlmake tool. The function creates virtual
  (temporary) Manifest.py file, populates its contents and retreives
  dependencies calling 'hdlmake list-json' command. The JSON is converted
  to dict and returned to the caller.

  Return:
  A list with dicts for the retreived dependencies in a form:
  [{'file': '...', 'language': '...', 'library': '...'}, {...}, {...}]
  '''
  # create temporary file
  cwd = os.getcwd()
  fd = tempfile.NamedTemporaryFile(mode='w', dir=cwd)

  # link temporary file 'Manifest.py'
  os.link(fd.name, "Manifest.py")

  #for target in path_target:
  # construct 'Manifest.py'
  fd.write('action   = "simulation"\n')
  fd.write('sim_tool = "' + sim_tool  + '"\n')
  fd.write('vcom_opt = "' + sim_opts  + '"\n')
  fd.write('sim_top  = "' + path_target.split('/')[-1].split('.')[0] + '"\n\n')

  fd.write('files   = ["' + path_target + '"]\n\n')
  fd.write('modules = {"local" : ["' + path_repo + '"]}')
  fd.flush()

  # aggregate dependencies using hdlmake
  dependencies = subprocess.check_output("hdlmake list-json", shell=True)

  # unlink 'Manifest.py'
  os.unlink("Manifest.py")

  # close temporary file
  fd.close()

  return json.loads(dependencies)


def get_dependencies(path_top, path_repo):
  return get_dependencies_hdlmake(path_top, path_repo)
