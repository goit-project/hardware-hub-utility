from goit.defines import Solver as Enum
from goit.classes.dependencies.DependencySolverHDLMake import DependencySolverHDLMake

def find_and_init(solver_id):
  if solver_id == Enum.DEFAULT \
  or solver_id == Enum.HDLMAKE:
    return DependencySolverHDLMake()

  raise("Framework type not supported!")
