from goit.defines import Solver as Enum

class Solver():
  '''
  Dependency solver super class.
  ''' 

  def __init__(self):
    '''TODO: documentation'''
    self.id = Enum.NONE


  def populate_dependencies(self, wildcard):
    '''TODO: documentation'''
    '''
    Aggregates and internally stores a list of files required to compile/
    simulate target component.

    Arguments:
    wildcard (string): A wildcard-type path to the component(s) for which
      dependency list must be populated.
    '''
    raise NotImplementedError()


  def get_dependencies(self):
    '''
    Return:
    A list of dicts values with component implementation files, libraries
    and optionally other metadata.
    '''
    raise NotImplementedError()
