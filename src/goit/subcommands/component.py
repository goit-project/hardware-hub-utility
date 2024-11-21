import argparse
import os
from goit import repository
from goit import dependencies

from goit.classes.ComponentVHDL import ComponentVHDL

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Instantiate component into the repository"


def command_callback(args):
  lib_paths     = dependencies.get_library_paths()
  repo_path     = repository.repo_getAbsolutePath()
  template_path = ComponentVHDL.template_path
  lib_subdir    = ComponentVHDL.lib_subdir

  # Check if template_path exists
  if not templates_exists(template_path):
    print("No matching templates were found here:", template_path)
    print("Did you forget to add them using the post-install scripts using pdm run all?")
    return
  
  # Check if is in repository
  if not repo_path:
    return

  # Uses the path base name as the library name if -l is not set
  if args.lname is not None: 
    lib_name = args.lname
  else:
    lib_name = os.path.basename(args.lpath)

  # Uses subdierectory for library components 
  if not args.force:
     root_comp = os.path.join(args.lpath, lib_subdir)
  else:
     root_comp = args.lpath

  print("Library name:       ", lib_name)
  print("Component name:     ", args.name)
  print("Component dest path:", os.path.join(root_comp, args.name))

  if(not os.path.exists(root_comp)):
     print("It is recommended to add new components to <library path>/{}, but there is no such directory. Use -p to set library path or -f to ignore.".format(lib_subdir))
     print("Existing library paths:")
     for path in lib_paths:
        print(" ",path)
     return

  comp_path = os.path.join(root_comp, args.name)
  if(os.path.exists(comp_path)):
     print("Directory: {} already conatains component named: {}".format(root_comp, args.name))
     return

  comp_VHDL = ComponentVHDL(comp_path, lib_name)


def add_command(subcommands, subparsers):
  '''Adds command callback and argument parsing logic to the main utility
     command given dict and subparse objects.

  Parameters
  ----------
    subcommands : dict
      dict object with a key-value form, where key is the name of the command
      and value corresponds to the command callback
        
    subparsers : argparse.subparsers
      subparsers object of the main command parser
  '''

  # add command
  subcommands[_CMD_NAME] = command_callback

  # add subparser and corresponding arguments
  parser = subparsers.add_parser(_CMD_NAME, help=_CMD_HELP)
  parser.add_argument("-n", "--name",  dest="name",  required=True,  help="name of the new component", type=str)
  parser.add_argument("-p", "--lpath", dest="lpath", required=False, help="path to an existing target library", type=lambda file_path: valid_path(parser, file_path), default=".")
  parser.add_argument("-f", "--force", dest="force", required=False, help="force component to be created in any existing directory", action='store_true')
  parser.add_argument("-l", "--lname", dest="lname", required=False, help="name of the target library", type=str)

def valid_path(parser, file_path):
  realpath = os.path.realpath(file_path)

  if not os.path.exists(file_path):
      parser.error("Library path {} does not exist!".format(realpath))
  else:
      return realpath

def templates_exists(template_path):
    '''Returns the template path if one exists, false otherwise'''
    if os.path.exists(template_path):
        return template_path
    
    return False