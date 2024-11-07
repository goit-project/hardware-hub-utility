import os

def repo_getAbsolutePath():
  ''' 
  Attempts to retreive repositories' base path given the current working
  directory (cwd), which is assumed to be inside the repository.
  '''

  # retreive current working directory
  cwd = os.getcwd()

  # recursevilly check all upper directories till "root" while checking for
  # the hidden repository marker file 'goit_repo_base'
  current_path = os.path.abspath(cwd)
  while not os.path.isfile(current_path + "/.goit_repository_base"):
    current_path = os.path.dirname(current_path)
    if current_path == '/':
      print("Failed to identify repository")
      return None

  return current_path 
