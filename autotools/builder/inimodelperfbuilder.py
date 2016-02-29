#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 模型性能参数构建器
    IniModelPerfBuilder
[model]
name=[model name]
count=[count of performances]

[perf<i>]
key=value
"""
import basebuilder
import baseitem

import time

import os

import web.template

render = web.template.render(os.path.split(os.path.realpath(__file__))[0],
globals={'type':type,"hasattr":hasattr})


class IniModelPerfBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(IniModelPerfBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        self.outfiles = []

    def CreateModelIni(self, item):
        props = baseitem.BaseItem(['md_name', 'md_ns', 'md_cname', 'md_desc', 'md_items'], item.item_val[:5])
        props.md_count = len(props.md_items)
        props.tm_now = time.ctime()

        if props.md_name[0] == 'S':
            return
        for i in range( props.md_count ):
            #Generate key
            props.it_id = i
            props.param = []

            name = props.md_items[i][1]
            if name == "":
                name = "%s-%d" % (props.md_cname, i+1)

            #Refine file name (convert reserved chars to char(_) )
            name = self.RefineFileName(name)

            for j in range( len(props.md_items[i]) ):
                param =  baseitem.BaseItem(['it_name', 'it_ns', 'it_cname', 'it_type', 'it_grain', 'it_unit', 'it_default', 'it_min', 'it_max', 'it_desc'], props.md_desc[j][:10] )
                param.it_val=props.md_items[i][j]

                props.param.append( param )

            self.WriteToFile(props.md_name, name, props)


    def WriteToFile(self, md_name, name, props):
        #Write to file
        folder = os.path.join(self.folder, md_name, "extend")
        name = os.path.join(folder, "%s.ini" %  name)

        ctx = render.pf_ini_tmpl(props)
        self.SaveFile(ctx, name, False)

    def Build(self):
        """ 根据性能参数写入ini文件 """
        for ns in self.GetNamespaces():
            for item in self.GetItemByNamespace(ns):
                if item.item_type == "ModelPerformance":#初始化参数
                    #print "ModelPerformance"
                    self.CreateModelIni(item);

    def GetFiles(self):
        outfiles = []
        for f in self.outfiles:
            outfiles.append( f.encode('utf-8') )
        return outfiles

