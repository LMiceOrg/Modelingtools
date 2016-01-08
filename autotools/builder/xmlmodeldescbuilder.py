#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" XMLModelDescBuilder
XML格式的模型描述建造者
"""

import basebuilder

import os
import re
import time
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

pother = re.compile(r'^([^_]+)[_]([^_]+)[_]([^.]+)[.]xls\w*')

class XMLModelDescBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(XMLModelDescBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        
        self.outfiles = []
        
    def CreateProjectNode(self, name, src):
        #Project node
        project = xmllib.Element("Project", {"Id":name,
                                                      "Name":name,
                                                      "Language":"C++" })
        xmllib.SubElement(project, "Description").text = "Generated at %s from %s" % (time.ctime(), src)
        
        self.elements[name]= {}
        self.elements[name]["Project"] = project
    def CreateComponentNode(self, name, src):
        com = xmllib.Element("Component", {"type":name, "category":"ModelComponent",
                                                         "GUID": "{%s}" % self.GetTypeUuid(name, "Constructive"),
                                                            "LVC_Feature":"Constructive"})

    
    def ParseItemSource(self, item):
        #Get pj_name from xlfile
        pj_num = ""
        pj_name = ""
        pj_cname = ""
        xlfile = os.path.split(item.source)[1]
        lv = pother.findall(xlfile)
        if len(lv) ==1 and len(lv[0]) == 3:
            pj_num = lv[0][0]
            pj_name = lv[0][1]
            pj_cname = lv[0][2]
        return pj_num, pj_name, pj_cname

    def CreateModelInitParamItem(self, data):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.ParseItemSource(item)
        if pj_num == "":
            return
        pps = xmllib.Element("Properties")
        pp_name, pp_cname, pp_items = data.item_val[:3]
        for item in pp_items:
            for i in range(len(item)):
                if item[i] == None:
                    item[i] = ""
                if type(item[i]) == str:
                    item[i] = item[i].decode('gbk')
                elif not type(item[i]) == unicode:
                    #print type(item[i]), type(item[i]) != unicode
                    item[i] = unicode(item[i])
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item
            pp = xmllib.SubElement(pps, "Property", {"Name":it_name, "ChineseName":it_cname})
            xmllib.SubElement(pp, "Description").text = it_desc
            xmllib.SubElement(pp, "Type", {"Namespace":it_ns,"Href":it_type, "HrefUuid":self.GetTypeUuid(it_type, it_ns)})
            #TODO: what are xsi:types of user defined types
            xmllib.SubElement(pp, "Default", {"Value":it_default, "xsi:type":"Types%sValue" % it_type})
        #insert into elements
        if not self.elements.has_key(pj_name):
            self.elements[pj_name]={}
        self.elements[pj_name]["Properties"] = pps
    def CreateModelMessageItem(self, item):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.ParseItemSource(item)
        if pj_num == "":
            return

        #Create in/out Message nodes
        innode = xmllib.Element("Inputs")
        outnode = xmllib.Element("Outputs")
    
    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        super(XMLModelDescBuilder, self).BuildBegin()

        if not os.path.isdir(self.folder):
            raise RuntimeError("folder(%s) is not exist!" % self.folder)
        
        self.elements = {}
        self.outfiles = []
    def Build(self):
        """开始构建 为每一个ModelInitParam创建一个XML对象 """
        for item in self.GetItems():
            if   item.item_type == "ModelMessage":    #模型消息
                self.CreateModelMessageItem(item)
            elif item.item_type == "ModelInitParam":    #模型参数
                self.CreateModelInitParamItem(item)
            elif item.item_type == "ModelEvent":    #模型事件
                self.CreateModelEventItem(item)
            elif item.item_type == "EnumData":  # 枚举类型
                self.AddEnumType(item)
            elif item.item_type == "CompData":  #复合数据结构
                self.AddCompType(item)
            elif item.item_type == "ArrayData": #数据类型
                self.AddArrayType(item)
