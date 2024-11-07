from enum import Enum
from goit import defines
from goit.classes.frameworks.FrameworkVUNIT import FrameworkVUNIT
from goit.classes.simulators.SimulatorGHDL  import SimulatorGHDL
from goit.classes.dependencies.DependencySolverHDLMake import DependencySolverHDLMake


def find_and_init_framework(framework_id, simulator=None):
  if framework_id == defines.Framework.DEFAULT \
  or framework_id == defines.Framework.VUNIT:
    return FrameworkVUNIT(simulator=simulator)

  raise("Framework type not supported!")


def find_and_init_simulator(simulator_id):
  if simulator_id == defines.Simulator.DEFAULT \
  or simulator_id == defines.Simulator.GHDL:
    return SimulatorGHDL()

  raise("Simulator type not supported!")


def find_and_init_solver(solver_id):
  if solver_id == defines.Solver.DEFAULT \
  or solver_id == defines.Solver.HDLMAKE:
    return DependencySolverHDLMake()

  raise("Framework type not supported!")
