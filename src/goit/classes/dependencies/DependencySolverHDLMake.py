from goit.classes.dependencies.DependencySolver import DependencySolver
from goit.dependencies import *


class DependencySolverHDLMake(DependencySolver):
  '''
  TODO
  ''' 

  def __init__(self):
    '''TODO: documentation'''


  def populate_dependencies(self, wildcard):
    '''TODO: documentation'''
    # retreive component list
    component_list = get_component_paths(wildcard)
    print(component_list)

    # retreive repo path
    # TODO

    # retreive dependencies using hdlmake
    #get_dependencies_hdlmake(path_repo, path_tb, sim_tool='ghdl', sim_opts='-2008'):


  def get_dependencies(self):
    '''
    Return:
    A list of dicts values with component implementation files, libraries
    and optionally other metadata.
    '''
    print("TODO")
