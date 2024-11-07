from enum import Enum

class Simulator(Enum):
  NONE    = 0   # not selected
  DEFAULT = 1   # attempt to detect simulator automatically
  GHDL    = 2   # open-source, https://github.com/ghdl/ghdl
  VSIM    = 3   # proprietary, modelsim/questa
  # others

class Solver(Enum):
  NONE    = 0   # not selected
  DEFAULT = 1   # attempt to detect simulator automatically
  HDLMAKE = 2   # open-source, https://ohwr.org/project/hdl-make
  # others

class Framework(Enum):
  NONE    = 0   # not selected
  DEFAULT = 1   # attempt to detect simulator automatically
  VUNIT   = 2   # open-source, https://vunit.github.io
  # others
