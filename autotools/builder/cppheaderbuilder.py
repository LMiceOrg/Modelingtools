#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CPPheaderBuilder
CPP头文件建造者
"""

import basebuilder

import time
import os
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

h_template=u"""
/****************************************************************************
**
**	开发单位：Dist3
**	开发者：hehao
**	创建时间：{tm_now}
**	版本号：V1.0
**	描述信息：{h_name}
****************************************************************************/
#ifndef {H_NAME}_H_
#define {H_NAME}_H_

namespace {h_name}
{{
{enumlist}
 {arraylist}
 {structlist}
}}

#endif //{H_NAME}_H_
"""

enumlist_template=u"""
enum {enum_name} {{
    {enum_element}
}};
"""

enum_template=u"""
{ENUM}={value}"""

arraylist_template=u"""
{array_type} {array_name}[{array_value}];"""

struct_template=u"""
struct xxx {{
AAA a;
double b;
}}
"""

class CPPHeaderBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(CPPHeaderBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        self.props={}   
        self.outfiles = []
        
        
    def CreateEnumCPPHeader(self, ed_ns, ctx):
        """ 生成枚举类型头文件的prop """
        ed_type, ed_desc, ed_items = ctx[:3]
        ed_id = "%s.%s" %(ed_ns, ed_type)
        listprop={}
        listprop["enum_name"] =ed_type
        listprop["enum_element"]= ''
        length=len(ed_items)
        i=1
        for item in ed_items:
            i=i+1
            enumprop={}
            it_name, it_value, it_desc = item[:3]
            it_id = "%s.%s" %(ed_id, it_name)
            it_value=int(it_value)
            enumprop["ENUM"] =('    ')+it_name
            if i<=length:
                enumprop["value"] =('{0}'.format(it_value))+(',')
            else :
                enumprop["value"] =('{0}'.format(it_value))
            ctx = enum_template.format(** enumprop)
            listprop["enum_element"] =listprop["enum_element"]+ctx 
        ctx = enumlist_template.format(** listprop)  
        self.props["enumlist"] = self.props["enumlist"]+ctx
        
    def CreateArrayCPPHeader(self, ad_ns, ctx):
        """ 生成数组类型头文件的prop """
        ad_name, ad_desc, ad_type, ad_dim = ctx[:4]
        ad_id = "%s.%s" %(ad_ns, ad_name)
        listprop={}
        listprop["array_type"] =('    ')+ad_type[6:10].lower()
        listprop["array_name"]= ad_name
        listprop["array_value"]= ad_type[11:-1] 
        ctx = arraylist_template.format(** listprop)  
        self.props["arraylist"] = self.props["arraylist"]+ctx

    def CreateCompCPPHeader(self,item):
        """ 生成复合结构体类型头文件的prop """

        
    def writeCPPHeaderFile(self):
        """ 写头文件 """
        ctx = h_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "%s.h" % self.props["h_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
     
    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        self.elements = {}
        self.outfiles = []
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个CPP头文件 """
        #创建Namespace element
        for ns in self.GetNamespaces():#namespace表示各种不同的类，平台类、传感器器类，
            self.props = {}
            self.props["tm_now"] =time.strftime("%Y-%m-%d %H:%M:%S")
            self.props["h_name"] =ns
            self.props["pj_path"] =self.folder
            self.props["H_NAME"] = ns.upper()
            self.props["enumlist"]=''
            self.props["arraylist"]=''
            self.props["structlist"]=''
            for item in self.GetItemByNamespace(ns):
                if item.item_type == "EnumData":    #枚举类型
                    #print "enum item"
                    self.CreateEnumCPPHeader(item.item_ns, item.item_val)#在头文件中加入值
                elif item.item_type == "ArrayData":   #数组类型
                    #print "array"
                    self.CreateArrayCPPHeader(item.item_ns, item.item_val)
                elif item.item_type == "CompData":    #复合结构
                    self.CreateCompCPPHeader(item)
            self.writeCPPHeaderFile()

    def BuildEnd(self):
        """结束构建 关闭所有头文件 """
        '''for ns in self.elements:
            root = self.elements[ns]
            self.SaveNamespaceFile(ns, root)'''

    def GetFiles(self):
        return self.outfiles
