from goit.defines import Simulator as Enum
from goit.classes.simulators.SimulatorGHDL import SimulatorGHDL

def find_and_init(simulator_id):
  if simulator_id == Enum.DEFAULT \
  or simulator_id == Enum.GHDL:
    return SimulatorGHDL()

  raise("Simulator type not supported!")
