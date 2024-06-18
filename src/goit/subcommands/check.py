import os

from goit.classes.CheckVHDL import CheckVHDL

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Perform codebase check"


def command_callback(args):
  if args.extension == "vhd":
    for path in args.paths:
      if path.endswith('.' + args.extension):
        check    = CheckVHDL(path, CheckVHDL.config())
        elements = check.analyze(check.document, check.config)
        
        if args.stats:
          header = "STATS: {}".format(check.file_path)
          print("-" * len(header))
          print(header)
          print("-" * len(header))
          
          for line in check.stats(elements, check.config):
            print(line)
        
        if args.demo:
          header = "DEMO: {}".format(check.file_path)
          print("-" * len(header))
          print(header)
          print("-" * len(header))
          
          for line in check.demo(elements):
            print(line)

        if args.compact:
          data    = check.compact(elements)
          res_map = {0: "no", 1: "yes"}
          c0_map  = {'r':'\x1b[38;2;180;0;0m', 'y':'\x1b[38;2;180;180;0m', 'g':'\x1b[38;2;0;180;0m'}
          c1      = '\x1b[0m'

          header = "COMPACT: {}".format(check.file_path)
          print("-" * len(header))
          print(header)

          author = 0
          if "@author" in data.keys():
            author = "{:13}: {c0}{}{c1}".format("author", ", ".join(data["@author"]), c0=c0_map["g"], c1=c1)
          else:
            author = "{:13}: {c0}{}{c1}".format("author", res_map[author], c0=c0_map["r"], c1=c1)
          print(author)

          entity   = 0
          brief    = 0
          detailed = 0
          if "entity" in data.keys():
            for entry in data["entity"]:
              brief    = entry["@brief"]    if "@brief"    in entry.keys() else brief
              detailed = entry["@detailed"] if "@detailed" in entry.keys() else detailed

              entity = "entity:\n    {:9}: {}\n    {:9}: {}".format("brief", res_map[brief], "detailed", res_map[detailed])
              print(entity)
          else:
            entity = "entity: {}".format(res_map[entity])
            print(entity)

          param = 0
          if "generic_param" in data.keys():
            tot, doc = data["generic_param"]
            if doc == 0:
              param = "{:13}: {c0}{}{c1}".format("generic_param", str(tot)+"/"+str(doc), c0=c0_map["r"], c1=c1)
            elif doc < tot:
              param = "{:13}: {c0}{}{c1}".format("generic_param", str(tot)+"/"+str(doc), c0=c0_map["y"], c1=c1)
            else:
              param = "{:13}: {c0}{}{c1}".format("generic_param", str(tot)+"/"+str(doc), c0=c0_map["g"], c1=c1)
          else:
            param = "{:13}: {c0}{}{c1}".format("generic_param", res_map[param], c0=c1, c1=c1)
          print(param)
          
          signal = 0
          if "port_signal" in data.keys():
            tot, doc = data["port_signal"]
            if doc == 0:
              signal = "{:13}: {c0}{}{c1}".format("port_signal", str(tot)+"/"+str(doc), c0=c0_map["r"], c1=c1)
            elif doc < tot:
              signal = "{:13}: {c0}{}{c1}".format("port_signal", str(tot)+"/"+str(doc), c0=c0_map["y"], c1=c1)
            else:
              signal = "{:13}: {c0}{}{c1}".format("port_signal", str(tot)+"/"+str(doc), c0=c0_map["g"], c1=c1)
          else:
            signal = "{:13}: {c0}{}{c1}".format("port_signal", res_map[signal], c0=c1, c1=c1)
          print(signal)

          # print(check.compact(elements))


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
  parser.add_argument("-i", dest="paths",  required=True,  help="paths of the input files to check", nargs='+', type=lambda file_path: valid_path(parser, file_path))
  parser.add_argument("-e", dest="extension", required=False, help="chooses how to interpret the file", default="vhd", choices=["vhd", "py"])
  parser.add_argument("-d", "--demo",  dest="demo",  required=False, help="prints the pseudo-structure of the file", action='store_true')
  parser.add_argument("-s", "--stats", dest="stats", required=False, help="prints the statistics of found commands and elements", action='store_true')
  parser.add_argument("-c", "--compact", dest="compact", required=False, help="prints compact file analysis result", action='store_true')


def valid_path(parser, file_path):
  if not os.path.exists(file_path):
      parser.error("The file %s does not exist!" % file_path)
  else:
      return file_path
