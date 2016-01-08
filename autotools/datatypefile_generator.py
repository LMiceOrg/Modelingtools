#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  数据类型定义文件生成类

"""

import os
import sys
import re
import hashlib as md5
import time
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

from __init__ import *
import projectmodel

class DataTypeFileGenerator:
    def __init__(self, name, **kw):
        if type(kw) == dict:
            self.__dict__ = kw
        self.name = name
        #初始化数据类型定义
        self.dt = projectmodel.DataType()
        #self.dt.ImportXML(simapp_dtfile)
        #初始化xml Element列表
        self.xdict={}
    #Customizing attribute access 'obj.name'
    def __getattr__(self, name):
        name = name.lower()
        if self.__dict__.has_key(name):
            return self.__dict__[name]
        else:
            return ""
            #raise AttributeError("The [%s] is not a valid attribute" % name)
    def __setattr__(self, name, value):
        name = name.lower()
        self.__dict__[name] = value
    def __delattr__(self, name):
        if self.__dict__.has_key(name):
            self.__dict__.pop(name)
    def VerifyNsName(self, ns, name):
        if dt_mapping.has_key(name):
            ns = dt_mapping[name][1]
            name = dt_mapping[name][0]
        elif ns == '' or ns == None:
            ns = default_ns_name
        return ns,name
    def Save(self, all_in_one=False):
        """ 生成数据结构XML 文件 """
        #if all_in_one != False:
        #    self.name = filename
        #print xmllib.tostring(self.root, 'utf-8')
        print "Call Save"
        flist=[]
        for ns in self.xdict:
            if self.xdict[ns] != None:
                doc = minidom.parseString( xmllib.tostring(self.xdict[ns], 'utf-8') )
                fname = "%s.xml" % ns
                #print fname
                x = doc.toprettyxml(encoding="utf-8")
                f = open(fname, "w")
                f.write(x)
                #f.write(xmllib.tostring(g.root, 'utf-8'))
                f.close()
                flist.append(os.path.abspath(fname))
        return flist
    def GenerateUUIDByName(self, name, ns=None):
        """ Generate UUID """
        if ns != None:
            name = ns + "." + name
        s = md5.md5(md5.md5(name).hexdigest()).hexdigest()
        return "-".join( (s[:8],s[8:12], s[12:16], s[16:20],s[20:]) ).upper()
    def GetNamespaceNode(self):
        """ 获取命名空间接点对象, 如果不存在则新建"""
        if self.root == None:
            self.GenerateRootNode()
        if self.root == None:
            raise ValueError("XML ElementTree internal error")

        node = self.root.find("Namespace")
        if node == None:
            node = xmllib.SubElement(self.root, "Namespace", {"Id":self.ns, "Name":self.ns})
            xmllib.SubElement(node, "Description").text = "It is the data type definition of namespace named %s ." % self.ns
        return node

    def GenerateRootNode(self):
        """ 新建根接点 """
        self.root = xmllib.Element("Catalogue:Catalogue", {"Id":"%sDataType" % self.name,
                                                      "Name":"%sDataType" % self.name,
                                                      "xmlns:Types":"http://www.appsoft.com.cn/Core/Types",
                                                      "xmlns:xlink":"http://www.w3.org/1999/xlink",
                                                      "xsi:schemaLocation":"http://www.appsoft.com.cn/Core/Catalogue Core/Catalogue.xsd",
                                                      "xmlns:Catalogue":"http://www.appsoft.com.cn/Core/Catalogue",
                                                      "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})
        xmllib.SubElement(self.root, "Description").text = "It is the definition file of namespace named %s" % self.ns
        xmllib.SubElement(self.root, "Import", {"Namespace":"AppSim", "Location":"AppSim"})
    def GetNsKeyBySheetName(self, name):
        for k in self.nslist:
            if name.find(self.nslist[k][0]) >= 0:
                return k
    def GetXmlElementByPublicSheetName(self, name):
        nskey = self.GetNsKeyBySheetName(name.encode('utf-8'))
        if nskey == None:
            print "NOT found Sheet name", name.encode('gbk')
            return
        nsvalue = self.nslist[nskey]
        if nsvalue == None:
            raise ValueError("Sheet name[%s] error" % name.encode('utf-8'))
        self.ns = nsvalue[1]
        if self.xdict.has_key(self.ns):
            self.root = self.xdict[self.ns]
        else:
            self.root = None
    def GetXmlElementByCustomExcelName(self, name):
        key = name[0] + '_'
        if not self.nslist.has_key(key):
            key = default_ns_key
        nsvalue = self.nslist[key]
        self.ns = nsvalue[1]
        if self.xdict.has_key(self.ns):
            self.root = self.xdict[self.ns]
        else:
            self.root = None
    def GeneratePublicArrayDataType(self, name, ctx):
        """ 由公共数组定义文件生成数组类型
        Excel struct: 数组数据类型名称	数据类型描述	数据类型	数组维数
        """

        # prepare the root element of data xml
        self.GetXmlElementByPublicSheetName(name)

        node = self.GetNamespaceNode()
        for i in range(1, len(ctx)):
            if len(ctx[i]) < 4:
                continue
            ad_name, ad_desc, ad_type, ad_dim = ctx[i][:4]
            ad_id = "%s.%s" %(self.ns, ad_name)

            #ignore empty row
            if ad_name == "":
                continue

            print "Array name", self.ns

            tnode = xmllib.SubElement(node, "Type", {"Id":ad_id,
            "Uuid":self.GenerateUUIDByName(ad_id),"Name":ad_name, "DataType":ad_type,
            "xsi:type":"Types:PrimitiveType"} )
            xmllib.SubElement(tnode, "Description").text = ad_desc
        # write back to xdict
        self.xdict[self.ns] = self.root
    def GeneratePublicEnumDataType(self, name, ctx):
        """由公共数据类型定义文件生成枚举类型
        Excel struct: 枚举数据类型名称	数据类型描述	枚举项	值	值定义
        """
        # prepare the root element of data xml
        self.GetXmlElementByPublicSheetName(name)

        last_ed_type = ''
        last_ed_desc = ''
        last_ed_items = []
        for i in range(1, len(ctx)):
            if len(ctx[i])<5:
                continue
            ed_type, ed_desc, it_name, it_value, it_desc = ctx[i][:5]
            if ed_type != "":
                if last_ed_type != "":
                    self.GenerateEnumData(self.ns, last_ed_type, last_ed_desc, last_ed_items)
                #new enumdata
                last_ed_type = ed_type
                last_ed_desc = ed_desc
                last_ed_items = []
            #append item data
            last_ed_items.append((it_name, it_value, it_desc))
        #process the last one
        if len(last_ed_items) >0:
            self.GenerateEnumData(self.ns, last_ed_type, last_ed_desc, last_ed_items)
        #write back to xdict
        self.xdict[self.ns] = self.root
    def GenerateEnumData(self, ed_ns, ed_type, ed_desc, ed_items):
        """ 生成枚举类型 """
        ed_id = "%s.%s" %(ed_ns, ed_type)
        node = self.GetNamespaceNode()
        tnode = xmllib.SubElement(node, "Type", {"Id": ed_id,"Name":ed_type,
                                         "Uuid": self.GenerateUUIDByName(ed_id),
                                         "xsi:type":"Types:Enumeration",
                                         "Description":ed_desc} )
        for item in ed_items:
            it_name, it_value, it_desc = item
            it_id = "%s.%s" %(ed_id, it_name)
            xmllib.SubElement(tnode, "Literal", {"Id":it_id,"Name":it_name,
                                                "Value":str(int( it_value ) ),
                                                "Description":it_desc})
            #print key

    def GeneratePublicCompDataType(self, name, ctx):
        """由公共数据类型定义文件生成复合数据结构
        Excel struct: (复合结构数据类型名称 ns 数据类型描述 数据项名称 ns1
        数据项中文名称 数据项数据类型 粒度 单位 默认值 最小值 最大值 数据项描述)
        """
        # prepare the root element of data xml
        self.GetXmlElementByPublicSheetName(name)


        last_cp_name=""
        last_cp_ns = ""
        last_cp_desc =""
        last_cp = []
        #枚举行
        for i in range(1, len(ctx)):
            if len(ctx[i]) <13:
                continue
            cp_name, cp_ns, cp_desc, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = ctx[i][:13]
            cp_ns = self.ns

            cp_name = cp_name.strip()
            it_name = it_name.strip()
            it_ns   = it_ns.strip()
            it_type = it_type.strip()
            cp_ns, cp_name = self.VerifyNsName(cp_ns, cp_name)
            #print "Original:", it_ns, it_type
            it_ns, it_type= self.VerifyNsName(it_ns, it_type)

            #print "Result:",it_ns, it_type
            # if got new compdata name
            if cp_name != "":
                # if has already got compdata ctx
                if last_cp_name != "" and len(last_cp) > 1:
                    self.GenerateCompData(last_cp_name, last_cp_ns, last_cp_desc, last_cp)
                # new compdata
                last_cp_name = cp_name
                last_cp_ns = cp_ns
                last_cp_desc = cp_desc
                last_cp = []
            # append item data
            last_cp.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc] )
        # process the last compdata
        if len(last_cp) >0:
            self.GenerateCompData(last_cp_name, last_cp_ns, last_cp_desc, last_cp)
        #write back to xdict
        self.xdict[self.ns] = self.root
    def GenerateCompData(self, cp_name, cp_ns, cp_desc, items):
        """ 生成复合数据结构 """

        node = self.GetNamespaceNode()
        cp_id = "%s.%s" %(cp_ns, cp_name)
        tnode = xmllib.SubElement(node, "Type", {"Id": cp_id,"Name":cp_name,
                                         "Uuid": self.dt.GetUuid(cp_ns, cp_name),
                                         "xsi:type":"Types:Structure",
                                         "Description":cp_desc} )
        for item in items:
            for i in range(len(item)):
                if item[i] == None:
                    item[i] = ""
                if type(item[i]) not in (str, unicode):
                    #print type(item[i]), type(item[i]) != unicode
                    item[i] = str(item[i])
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item
            it_id = "%s.%s" %(cp_id, it_name)
            fnode = xmllib.SubElement(tnode, "Field", {"Id": it_id, "Name":it_name,
            "Description":it_desc, "Unit":it_unit, "ChineseName":it_cname, "GrainSize": it_grain,
            "Default":it_default, "Min":it_min, "Max":it_max})
            xmllib.SubElement(fnode, "Type", {"Namespace":it_ns, "Href":it_type,"HrefUuid":self.dt.GetUuid(it_ns, it_type) })

    def GeneratorCustomCompDataType(self, xl_file, sh_name, ctx):
        """由模型数据类型定义文件生成复合数据结构
        Excel struct: (消息名称 ns1 中文名称 输入输出类型 接口描述 是否可变长 变量名称
        ns2 变量中文名称 变量数据类型 粒度 单位 默认值 最小值 最大值 参数描述 赋值方法)
        """
        # prepare the root element of data xml
        self.GetXmlElementByCustomExcelName(xl_file)


        last_cp_name=""
        last_cp_ns = ""
        last_cp_desc =""
        last_cp = []
        #枚举行
        for i in range(1, len(ctx)):
            cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_vlen, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc, it_assign = ('',)*17
            if len(ctx[i]) == 15:
                cp_ns = self.ns
                it_ns = self.ns
                cp_name, cp_cname, cp_io, cp_desc, cp_vlen, it_name = ctx[i][:6]
                it_cname, it_type, it_grain, it_unit, it_default = ctx[i][6:11]
                it_min,it_max, it_desc, it_assign = ctx[i][-4:]
            elif len(ctx[i]) >= 17:
                cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_vlen, it_name = ctx[i][:7]
                it_ns, it_cname, it_type, it_grain, it_unit, it_default = ctx[i][7:13]
                it_min, it_max, it_desc, it_assign = ctx[i][-4:]
            else:
                continue
            cp_ns = self.ns
            cp_name = cp_name.strip()
            it_name = it_name.strip()
            it_ns   = it_ns.strip()
            it_type = it_type.strip()
            #check input
            if it_name == "" or it_type == "" or it_ns== "":
                continue
            #verify namespace
            cp_ns, cp_name = self.VerifyNsName(cp_ns, cp_name)
            #print "Original:", it_ns, it_type
            it_ns, it_type= self.VerifyNsName(it_ns, it_type)

            #print "Result:",it_ns, it_type
            # if got new compdata name
            if cp_name != "":
                # if has already got compdata ctx
                if last_cp_name != "" and len(last_cp) > 1:
                    self.GenerateCompData(last_cp_name, last_cp_ns, last_cp_desc, last_cp)
                # new compdata
                last_cp_name = cp_name
                last_cp_ns = cp_ns
                last_cp_desc = cp_desc
                last_cp = []
            # append item data
            last_cp.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc] )
        # process the last compdata
        if len(last_cp) >1:
            self.GenerateCompData(last_cp_name, last_cp_ns, last_cp_desc, last_cp)
        #write back to xdict
        self.xdict[self.ns] = self.root
