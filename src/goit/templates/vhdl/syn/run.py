#!/usr/bin/env python3
import edi_ic_routines as edi

# This is a template python script for setting up simple synthesis project. The
# edi_ic_routines.py" script file, should be added to the PYTHONPATH, see
# setup.sh

# generate synthesis project with "main" as top entity
edi.synthesis_setupProject("../src/*.vhd", topEntity="main")
