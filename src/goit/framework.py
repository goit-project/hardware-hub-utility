from goit.defines import Framework as Enum
from goit.classes.frameworks.FrameworkVUNIT import FrameworkVUNIT

def find_and_init(framework_id, simulator=None):
  if framework_id == Enum.DEFAULT \
  or framework_id == Enum.VUNIT:
    return FrameworkVUNIT(simulator=simulator)

  raise("Framework type not supported!")
