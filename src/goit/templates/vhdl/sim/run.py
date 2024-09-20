#!/usr/bin/env python3
import edi_ic_routines as edi

# This is a template python script for setting up vunit based simulation. The
# edi_ic_routines.py" script file, should be added to the PYTHONPATH, see
# setup.sh

# set up Vunit project and dependencies
[prj, tbLib] = edi.vunit_setupProjectAddDeps("../src/*.vhd", "../tb/*.vhd")

# TODO: remove
# Example for passing generic configuration to the testbench(es)
#tbLib.test_bench("tb").test("test_name").add_config(
#  name="title_of_the_test_configuration",
#  generics=dict(
#    GENERIC_CONSTANT0 = 777,
#    GENERIC_CONSTANT1 = #deadbeef))

# Run vunit function
prj.main()
