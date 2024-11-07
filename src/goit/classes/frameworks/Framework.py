from goit.defines import Framework as Enum
from goit.classes.simulators.Simulator import Simulator


class Framework():
  def __init__(self):
    self.id = Enum.NONE
    pass
 
  def add_library(self, library):
    raise("Framework method not implemented!")

  def add_source_file(self, library, filepath):
    raise("Framework method not implemented!")

  def run():
    raise("Framework method not implemented!")
