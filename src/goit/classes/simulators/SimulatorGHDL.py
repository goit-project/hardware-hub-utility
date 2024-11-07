from goit.defines import Simulator as Enum
from goit.classes.simulators.Simulator import Simulator


class SimulatorGHDL(Simulator):
  def __init__(self):
    self.id = Enum.GHDL
