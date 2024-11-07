import os
from vunit import VUnit
from goit.defines import Framework as Enum
from goit.defines import Simulator as EnumSimulator
from goit.classes.frameworks.Framework import Framework


class FrameworkVUNIT(Framework):
  def __init__(self, simulator=None):
    self.id = Enum.VUNIT

    # use environment variables to guide the use of simulator
    if simulator:
      if simulator.id == EnumSimulator.GHDL:
        print("===== 1 =====")
        os.environ["VUNIT_SIMULATOR"] = "ghdl"
      elif simulator.id == EnumSimulator.VSIM:
        print("===== 2 =====")
        os.environ["VUNIT_SIMULATOR"] = "vsim"

    # initialize framework and add default simulation libraries
    self.prj = VUnit.from_argv()
    self.prj.add_osvvm()
    self.prj.add_verification_components()

  def add_library(self, library):
    # it is not permitted to create "work" (default) library
    if library  == "work"\
    or library  == "vunit_lib"\
    or library  == "osvvm":
      return

    # check if library has not been already added
    library_list = self.prj.get_libraries()
    for l in library_list:
      if l.name == library:
        return

    # add the library
    print(' - adding library: %s' % (library))
    self.prj.add_library(library)


  def add_source_file(self, library, filepath):
    # "vunit_lib" and "osvvm" library components are already added by default
    if library  == "work"\
    or library  == "vunit_lib"\
    or library  == "osvvm":
      return

    print(" - adding source file: %s <= \"%s\"" %(library, filepath))
    self.prj.library(library).add_source_file(filepath)


  def run(self):
    self.prj.main()
