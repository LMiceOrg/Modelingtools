#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 工程文件生成
so_ 模块方案
pj_ 模块工程
tp_ 测试工程
"""
import basebuilder

import os
import hashlib as md5

import web.template

render = web.template.render(os.path.join( os.path.split(os.path.realpath(__file__))[0], "template") ,
globals={'type':type,"hasattr":hasattr})

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
        if not os.path.exists(self.props["pj_path"]):
            os.makedirs(self.props["pj_path"])
        if not os.path.exists(self.props["tp_path"]):
            os.makedirs(self.props["tp_path"])
        return

    def BuildSolutionFile(self):
        #print self.props.keys
        ctx = render.msvc2008_sln_tmpl(self.props)
        name = os.path.join(self.props["so_path"], "%s.sln" % self.props["so_name"])
        f=open(name, "w")
        f.write( str(ctx) )
        f.close()
        return name

    def BuildSolution(self, pps):
        self.props = pps
        self.BuildProjectFolder()
        return self.BuildSolutionFile()

