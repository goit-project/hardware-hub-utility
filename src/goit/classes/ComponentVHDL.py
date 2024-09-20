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

        comp_name = os.path.basename(comp_path)
        os.mkdir(comp_path)
        
        for dir, files in self.template_struct.items():
            dir_path = os.path.join(comp_path, dir)
            os.mkdir(dir_path)

            for file, enbled in files.items():
                if enbled:
                    src_path = os.path.join(self.template_path, dir, file)
                    dst_path = os.path.join(dir_path, file)
                    shutil.copy(src_path, dst_path)

            if dir == "src":
                self.prepare_src(dir_path, comp_name)
            elif dir == "tb":
                self.prepare_tb(dir_path, comp_name, lib_name)
            elif dir == "sim":
                self.prepare_sim()
            elif dir == "syn":
                self.prepare_syn(dir_path, comp_name, lib_name)


    def prepare_src(self, dir_path, comp_name):
        fname = comp_name + ".vhd"
        fpath_src = os.path.join(dir_path, "component.vhd")
        fpath_dst = os.path.join(dir_path, fname)
        os.rename(fpath_src, fpath_dst)

        with open(fpath_dst) as file:
            filedata = file.read()
            filedata = filedata.replace("/*file name*/", fname)
            filedata = filedata.replace("/*component name*/", comp_name)
        with open(fpath_dst, "w") as file:
            file.write(filedata)


    def prepare_tb(self, dir_path, comp_name, lib_name):
        fpath = os.path.join(dir_path, "tb.vhd")
        with open(fpath) as file:
            filedata = file.read()
            filedata = filedata.replace("/*lib*/", lib_name)
            filedata = filedata.replace("/*entity*/", comp_name)
        with open(fpath, "w") as file:
            file.write(filedata)


    def prepare_syn(self, dir_path, comp_name, lib_name):
        fpath = os.path.join(dir_path, "main.vhd")
        with open(fpath) as file:
            filedata = file.read()
            filedata = filedata.replace("/*lib*/", lib_name)
            filedata = filedata.replace("/*entity*/", comp_name)
        with open(fpath, "w") as file:
            file.write(filedata)


    def prepare_sim(self):
        pass
