#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Build model Vislual Studio 2008 solution files

"""

import xmlmodeldescbuilder
import msvc2008solutionbuilder

import msvc2008projectbuilder

import qt5builder

import os
import time

class Msvc2008Builder(xmlmodeldescbuilder.XMLModelDescBuilder):
    def __init__(self, datamodel, folder):
        super(Msvc2008Builder, self).__init__(datamodel, folder)

        self.sobuilder = msvc2008solutionbuilder.Msvc2008SolutionBuilder()
        self.pjbuilder = msvc2008projectbuilder.Msvc2008ProjectBuilder()
        self.qt5builder = qt5builder.Qt5Builder(datamodel, folder)
    def BuildEnd(self):
        """写入 solution 文件 """
        for pj_name in self.elements:
            props = {}
            props["tm_now"] =time.strftime("%Y-%m-%d %H:%M:%S")
            props["pj_cname"] = self.projects[pj_name][3]
            props["src_path"] = self.projects[pj_name][0]

            props["so_folder"]= pj_name
            props["pj_folder"]="src"
            props["tp_folder"] = "test"
            props["root"] = self.folder
            props["so_name"] = pj_name + "Solution"
            props["pj_name"] = pj_name
            props["tp_name"] = "Test" + pj_name
            props["PJ_NAME"] = pj_name.upper()

            props["so_uuid"] = self.GenerateUUIDByName(props["so_name"], "MSVC2008")
            props["pj_uuid"] = self.GenerateUUIDByName(props["pj_name"], "MSVC2008")
            props["tp_uuid"] = self.GenerateUUIDByName(props["tp_name"], "MSVC2008")

            props["so_path"] = "{root}/code/{so_folder}".format(**props)
            props["pj_path"]=  os.path.join( props["so_path"], props["pj_folder"])
            props["tp_path"] = os.path.join( props["so_path"], props["tp_folder"])

            #create solution node
            so_file = self.sobuilder.BuildSolution(props)

            #create model project node
            pj_file = self.pjbuilder.BuildProject(props)
            #create test project node
            #self.GenerateComponentNode(pj_name, root)
            self.qt5builder.BuildSolution(props)
            self.qt5builder.BuildProject(props)


            #save to dsc file
            self.outfiles.append(so_file.encode('utf-8'))
    def GetFiles(self):
        return self.outfiles
