#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""生成Qt5工程文件

"""

solution_template=u"""#-------------------------------------------------
#
# Project created by Modelingtools {tm_now}
#
#-------------------------------------------------

TEMPLATE = subdirs

SUBDIRS += {pj_name} {tp_name}

{pj_name}.file = {pj_folder}/{pj_name}.pro
{pj_name}.subdirs = {pj_folder}

{tp_name}.file = {tp_folder}/{tp_name}.pro
{tp_name}.subdirs = {tp_folder}
{tp_name}.depends = {pj_name}


"""

pj_template=u"""#-------------------------------------------------
#
# Project created by Modelingtools {tm_now}
#
#   Generated from source: {src_path}
#-------------------------------------------------

TEMPLATE = lib

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

#CONFIG += xxx

TARGET = {pj_name}

SOURCES += {pj_name}.cpp

HEADERS += {pj_name}export.h \
    {pj_name}userdata.h \
    {pj_name}export.h

"""

tp_template=u"""#-------------------------------------------------
#
# Project created by Modelingtools {tm_now}
#
#   Generated from source: {src_path}
#-------------------------------------------------

TEMPLATE = app

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

#CONFIG += xxx

TARGET = {pj_name}

SOURCES += {pj_name}.cpp

HEADERS += {pj_name}export.h \
    {pj_name}userdata.h \
    {pj_name}export.h

"""

import xmlmodeldescbuilder

import os
import time

class Qt5Builder(xmlmodeldescbuilder.XMLModelDescBuilder):
    def __init__(self, datamodel, folder):
        super(Qt5Builder, self).__init__(datamodel, folder)

    def BuildProjectFolder(self):
        """ 生成工程文件路径和项目文件路径 root/code/{so_folder} """
        if not os.path.exists(self.props["pj_path"]):
            os.makedirs(self.props["pj_path"])
        if not os.path.exists(self.props["tp_path"]):
            os.makedirs(self.props["tp_path"])
        return

    def BuildSolutionFile(self):
        #print self.props.keys

        ctx = solution_template.format(** self.props)
        name = os.path.join(self.props["so_path"], "%s.pro" % self.props["so_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        return name

    def BuildSolution(self, pps):
        self.props = pps
        self.BuildProjectFolder()
        return self.BuildSolutionFile()

    def BuildProject(self, pps):
        files = []
        #project
        ctx = pj_template.format(**pps)
        name = os.path.join(pps["pj_path"], "%s.pro" % self.props["pj_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        files.append(name)

        #test project
        ctx = tp_template.format(**pps)
        name = os.path.join(pps["tp_path"], "%s.pro" % self.props["tp_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        files.append(name)

        return files

    def BuildEnd(self):
        """ 写入pro 文件 """
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

            props["so_uuid"] = self.GenerateUUIDByName(props["so_name"], "QT5")
            props["pj_uuid"] = self.GenerateUUIDByName(props["pj_name"], "QT5")
            props["tp_uuid"] = self.GenerateUUIDByName(props["tp_name"], "QT5")

            props["so_path"] = "{root}/code/{so_folder}".format(**props)
            props["pj_path"]=  os.path.join( props["so_path"], props["pj_folder"])
            props["tp_path"] = os.path.join( props["so_path"], props["tp_folder"])

            #create solution node
            so_file = self.BuildSolution(props)

            #create model project node
            pj_file = self.BuildProject(props)
            #create test project node
            #self.GenerateComponentNode(pj_name, root)


            #save to dsc file
            self.outfiles.append(so_file.encode('utf-8'))
    def GetFiles(self):
        return self.outfiles
