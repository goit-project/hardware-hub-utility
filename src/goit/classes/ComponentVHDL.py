import os
import shutil
from goit.classes.Component import Component

class ComponentVHDL(Component):
    """Documentation for a class.
    
    More details.
    """

    lib_subdir      = "components"
    template_path   = os.path.join(os.path.dirname(__file__), "../templates/vhdl")
    template_struct = {'src' : {'component.vhd': True},
                       'tb'  : {'tb.vhd'       : True},
                       'sim' : {'run.py'       : True},
                       'syn' : {'run.py'       : True, 'main.vhd' : True}}
    
    def __init__(self, comp_path, lib_name):
        """The constructor."""

        # Creates root for the component
        os.mkdir(comp_path)

        # Creates a sub-directory if any file is enabled
        for sub_dir in self.template_struct.keys():
            if any(self.template_struct[sub_dir].values()):
                os.mkdir(os.path.join(comp_path, sub_dir))

        # Copies all enabled files from the templates directory
        for sub_dir, fnames in self.template_struct.items():
            for fname, enbled in fnames.items():
                if enbled:
                    src_path = os.path.join(self.template_path, sub_dir, fname)
                    dst_path = os.path.join(comp_path, sub_dir, fname)
                    shutil.copy(src_path, dst_path)

        # Does file preparation
        for sub_dir in self.template_struct.keys():
            comp_name = os.path.basename(comp_path)
            sub_path  = os.path.join(comp_path, sub_dir)
            
            if sub_dir == "src":
                print('Preparing source file...')
                self.prepare_src(sub_path, comp_name)
            
            elif sub_dir == "tb":
                print('Preparing test bench...')
                self.prepare_tb(sub_path, comp_name, lib_name)
            
            elif sub_dir == "sim":
                print('Preparing simulation files...')
                self.prepare_sim()
            
            elif sub_dir == "syn":
                print('Preparing synthesis files...')
                self.prepare_syn(sub_path, comp_name, lib_name)

        print('Done')

    def prepare_src(self, dir_path, comp_name):
        fname     = comp_name + ".vhd"
        fpath_src = os.path.join(dir_path, "component.vhd")
        fpath_dst = os.path.join(dir_path, fname)
        
        if os.path.exists(fpath_src):
            os.rename(fpath_src, fpath_dst)
            self.replace_in_file(fpath_dst, "/*file name*/", fname)
            self.replace_in_file(fpath_dst, "/*component name*/", comp_name)


    def prepare_tb(self, dir_path, comp_name, lib_name):
        fpath = os.path.join(dir_path, "tb.vhd")
        
        if os.path.exists(fpath):
            self.replace_in_file(fpath, "/*lib*/", lib_name)
            self.replace_in_file(fpath, "/*entity*/", comp_name)


    def prepare_syn(self, dir_path, comp_name, lib_name):
        fpath = os.path.join(dir_path, "main.vhd")
        
        if os.path.exists(fpath):
            self.replace_in_file(fpath, "/*lib*/", lib_name)
            self.replace_in_file(fpath, "/*entity*/", comp_name)


    def prepare_sim(self):
        pass


    def replace_in_file(self, fpath, search_text, replace_text):
        with open(fpath, "r") as file:
            replaced = file.read().replace(search_text, replace_text)
        
        with open(fpath, "w") as file:
            file.write(replaced)

