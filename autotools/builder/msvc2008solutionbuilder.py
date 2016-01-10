#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 工程文件生成
so_ 模块方案
pj_ 模块工程
tp_ 测试工程
"""
solution_template = u"""
Microsoft Visual Studio Solution File, Format Version 10.00
# Visual Studio 2008

Project("{{{so_uuid}}}") = "{pj_name}", "{pj_folder}\{pj_name}.vcproj", "{{{pj_uuid}}}"
EndProject
Project("{{{so_uuid}}}") = "Test{pj_name}", "{tp_folder}\Test{pj_name}.vcproj", "{{{tp_uuid}}}"
        ProjectSection(ProjectDependencies) = postProject
                {{{pj_uuid}}} = {{{pj_uuid}}}
        EndProjectSection
EndProject
Global
        GlobalSection(SolutionConfigurationPlatforms) = preSolution
                Debug|Win32 = Debug|Win32
                Release|Win32 = Release|Win32
        EndGlobalSection
        GlobalSection(ProjectConfigurationPlatforms) = postSolution
                {{{pj_uuid}}}.Debug|Win32.ActiveCfg = Debug|Win32
                {{{pj_uuid}}}.Debug|Win32.Build.0 = Debug|Win32
                {{{pj_uuid}}}.Release|Win32.ActiveCfg = Release|Win32
                {{{pj_uuid}}}.Release|Win32.Build.0 = Release|Win32
                {{{tp_uuid}}}.Debug|Win32.ActiveCfg = Debug|Win32
                {{{tp_uuid}}}.Debug|Win32.Build.0 = Debug|Win32
                {{{tp_uuid}}}.Release|Win32.ActiveCfg = Release|Win32
                {{{tp_uuid}}}.Release|Win32.Build.0 = Release|Win32
        EndGlobalSection
        GlobalSection(SolutionProperties) = preSolution
                HideSolutionNode = FALSE
        EndGlobalSection
EndGlobal

"""

import basebuilder

import os
import hashlib as md5

class Msvc2008SolutionBuilder(object):
    def __init__(self):
        self.props = {}

    def GenerateUUIDByName(self, name, ns=None):
        """ Generate UUID """
        if ns != None:
            name = ns + "." + name
        if type(name) == unicode:
            name = name.encode('utf-8')
        s = md5.md5(md5.md5(name).hexdigest()).hexdigest()
        return "-".join( (s[:8],s[8:12], s[12:16], s[16:20],s[20:]) ).upper()

    def BuildProjectFolder(self):
        """ 生成工程文件路径和项目文件路径 root/code/{so_folder} """

        #self.props["pj_folder"]="src"
        #self.props["tp_folder"] = "test"
        #self.props["root"] = root_folder

        #self.props["so_name"] = pj_name + "Solution"
        #self.props["pj_name"] = pj_name
        #self.props["tp_name"] = "Test" + pj_name
        #self.props["PJ_NAME"] = pj_name.upper()

        #self.props["so_uuid"] = self.GenerateUUIDByName(self.props["so_name"], "MSVC2008")
        #self.props["pj_uuid"] = self.GenerateUUIDByName(self.props["pj_name"], "MSVC2008")
        #self.props["tp_uuid"] = self.GenerateUUIDByName(self.props["tp_name"], "MSVC2008")

        #if not self.props.has_key("so_folder"):
        #    self.props["so_folder"]="solution"

        #self.props["so_path"] = "{root}/code/{so_folder}".format(**self.props)
        #self.props["pj_path"]=  os.path.join( self.props["so_path"], self.props["pj_folder"])
        #self.props["tp_path"] = os.path.join( self.props["so_path"], self.props["tp_folder"])
        if not os.path.exists(self.props["pj_path"]):
            os.makedirs(self.props["pj_path"])
        if not os.path.exists(self.props["tp_path"]):
            os.makedirs(self.props["tp_path"])
        return

    def BuildSolutionFile(self):
        #print self.props.keys

        ctx = solution_template.format(** self.props)
        name = os.path.join(self.props["so_path"], "%s.sln" % self.props["so_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        return name

    def BuildSolution(self, pps):
        self.props = pps
        self.BuildProjectFolder()
        return self.BuildSolutionFile()

