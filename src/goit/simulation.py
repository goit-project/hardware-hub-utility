from glob import glob
from goit import defines
from goit import framework
from goit import solver
from goit import simulator

class Simulation:
  def __init__(self,
    framework_id = defines.Framework.DEFAULT,
    solver_id    = defines.Solver.DEFAULT,
    simulator_id = defines.Simulator.DEFAULT):

    # initialize simulation wrapper objects
    self.solver    = solver.find_and_init(solver_id)
    self.simulator = simulator.find_and_init(simulator_id)
    self.framework = framework.find_and_init(framework_id, simulator=self.simulator)

    # bookkeeping
    self._design_tests    = []
    self._design_sources  = []
    self._dependencies    = []


  def add_testbenches(self, *paths):
    # retrieve testbench files
    for path in paths:
      self._design_tests += glob(path)

    # use dependency solver to populate dependencies
    for path in paths:
      self.solver.populate_dependencies(path)

    # add populated dependencies to the internal list (TODO: avoid duplicates)
    self._dependencies += self.solver.get_dependencies()


  def add_sources(self, *paths):
    # retrieve source files
    for path in paths:
      self._design_sources += glob(path)

    # use dependency solver to populate dependencies
    for path in paths:
      self.solver.populate_dependencies(path)

    # add populated dependencies to the internal list (TODO: avoid duplicates)
    self._dependencies += self.solver.get_dependencies()


  def run(self):
    print('Adding libraries')
    for d in self._dependencies:
      self.framework.add_library(d['library'])

    print('Adding dependencies / source files')
    for i, d in enumerate(self._dependencies):
      self.framework.add_source_file(d['library'], d['file'])

    print('Adding test files')
    self.framework.add_library('test')
    for tb_file in self._design_tests:
      self.framework.add_source_file('test', tb_file)

    print('Executing framework')
    self.framework.run()
