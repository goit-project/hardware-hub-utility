from goit.defines import Solver as Enum
from goit.repository import *
from goit.dependencies import *
from goit.classes.dependencies.DependencySolver import DependencySolver


class DependencySolverHDLMake(DependencySolver):
  '''
  TODO
  ''' 

  def __init__(self):
    '''TODO: documentation'''
    self.id = Enum.HDLMAKE


  def populate_dependencies(self, wildcard):
    '''TODO: documentation'''
    # retreive component list
    path_targets = get_component_paths(wildcard)

    # retreive repo path
    path_repo = repo_getAbsolutePath()
    path_repo_rel = os.path.relpath(path_repo, os.getcwd())

    # retreive dependencies using hdlmake
    dependencies = []
    for path_target in path_targets:
      deps = get_dependencies_hdlmake(path_repo_rel, path_target, sim_tool='ghdl', sim_opts='-2008')
      for f in deps['files']:
        dependencies.append(f)

    # TODO: remove duplicates
    self.dependencies = dependencies


  def get_dependencies(self):
    '''
    Return:
    A list of dicts values with component implementation files, libraries
    and optionally other metadata.
    '''
    return self.dependencies
