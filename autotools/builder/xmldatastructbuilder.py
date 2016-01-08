#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" XMLDataStructBuilder
XML格式的数据结构建造者
"""

import basebuilder

import os
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

class XMLDataStructBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(XMLDataStructBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        
        self.outfiles = []
        
    def SaveNamespaceFile(self, ns, root):
        doc = minidom.parseString( xmllib.tostring(root, 'utf-8') )
        data = doc.toprettyxml(encoding="utf-8")
        name = os.path.join(self.folder, u"%s.xml" % ns)

        f = open(name, "w")
        f.write(data)
        f.close()
        self.outfiles.append(name.encode('utf-8'))
        
    def CreateNamespaceNode(self, root, ns):
        """ 命名空间接点对象, 如果不存在则新建"""
        
        node = xmllib.SubElement(root, "Namespace", {"Id":ns, "Name":ns})
        xmllib.SubElement(node, "Description").text = "It is the data type definition of namespace named %s ." % ns
        return root

    def CreateRootNode(self,ns):
        """ 新建根接点 """
        root = xmllib.Element("Catalogue:Catalogue", {"Id":"%sDataType" % self.name,
                                                      "Name":"%sDataType" % self.name,
                                                      "xmlns:Types":"http://www.appsoft.com.cn/Core/Types",
                                                      "xmlns:xlink":"http://www.w3.org/1999/xlink",
                                                      "xsi:schemaLocation":"http://www.appsoft.com.cn/Core/Catalogue Core/Catalogue.xsd",
                                                      "xmlns:Catalogue":"http://www.appsoft.com.cn/Core/Catalogue",
                                                      "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})
        xmllib.SubElement(root, "Description").text = "It is the data type definition file of namespace named %s" % ns
        xmllib.SubElement(root, "Import", {"Namespace":"AppSim", "Location":"AppSim"})
        return root

    def CreateEnumDataItem(self, node, ed_ns, ctx):
        """ 生成枚举类型 """
        ed_type, ed_desc, ed_items = ctx[:3]
        ed_id = "%s.%s" %(ed_ns, ed_type)
        tnode = xmllib.SubElement(node, "Type", {"Id": ed_id,"Name":ed_type,
                                         "Uuid": self.GetTypeUuid(ed_type, ed_ns),
                                         "xsi:type":"Types:Enumeration",
                                         "Description":ed_desc} )
        for item in ed_items:
            it_name, it_value, it_desc = item[:3]
            it_id = "%s.%s" %(ed_id, it_name)
            xmllib.SubElement(tnode, "Literal", {"Id":it_id,"Name":it_name,
                                                "Value":str(int( it_value ) ),
                                                "Description":it_desc})

    def CreateArrayDataItem(self, node, ad_ns, ctx):
        """ 生成数组类型 """
        #print "array"
        ad_name, ad_desc, ad_type, ad_dim = ctx[:4]
        ad_id = "%s.%s" %(ad_ns, ad_name)
        tnode = xmllib.SubElement(node, "Type", {"Id":ad_id,
            "Uuid":self.GetTypeUuid(ad_name, ad_ns),"Name":ad_name, "DataType":ad_type,
            "xsi:type":"Types:PrimitiveType"} )
        xmllib.SubElement(tnode, "Description").text = ad_desc

    def CreateCompDataItem(self, node, data):
        """ 生成复合结构体类型 """

        cp_ns = data.item_ns
        ctx = data.item_val
        cp_name, cp_desc, cp_items = ctx[:3]

        cp_id = "%s.%s" %(cp_ns, cp_name)
        #print type(data.part_name)
        tnode = xmllib.SubElement(node, "Type", {"Id": cp_id,"Name":cp_name,
                                         "Uuid": self.GetTypeUuid(cp_name, cp_ns),
                                         "xsi:type":"Types:Structure",
                                         "Description":cp_desc,
                                         "Source": "%s[%s]" %(data.source, data.part_name) } )
        for item in cp_items:
            for i in range(len(item)):
                if item[i] == None:
                    item[i] = ""
                if type(item[i]) not in (str, unicode):
                    #print type(item[i]), type(item[i]) != unicode
                    item[i] = str(item[i])
            #it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc
            #print len(item)
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item
            it_id = "%s.%s" %(cp_id, it_name)
            fnode = xmllib.SubElement(tnode, "Field", {"Id": it_id, "Name":it_name,
            "Description":it_desc, "Unit":it_unit, "ChineseName":it_cname, "GrainSize": it_grain,
            "Default":it_default, "Min":it_min, "Max":it_max})
            xmllib.SubElement(fnode, "Type", {"Namespace":it_ns, "Href":it_type,"HrefUuid":self.GetTypeUuid(it_type, it_ns) })
    def CreateModelMessageItem(self, node, data):
        """ 模型消息"""
        ctx = data.item_val
        cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cp_items = ctx[:7]

        cp_id = "%s.%s" %(cp_ns, cp_name)

        if len(cp_items) == 1:
            return
        
        #print type(data.part_name)
        tnode = xmllib.SubElement(node, "Type", {"Id": cp_id,"Name":cp_name,
                                         "Uuid": self.GetTypeUuid(cp_name, cp_ns),
                                         "xsi:type":"Types:Structure",
                                         "Description":cp_cname,
                                         "Source": "%s[%s]" %(data.source, data.part_name) } )
        for item in cp_items:
            for i in range(len(item)):
                if item[i] == None:
                    item[i] = ""
                if type(item[i]) == str:
                    item[i] = item[i].decode('gbk')
                elif not type(item[i]) == unicode:
                    #print type(item[i]), type(item[i]) != unicode
                    item[i] = unicode(item[i])
            #it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc
            #print len(item)
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc, it_asign = item
            it_id = "%s.%s" %(cp_id, it_name)
            fnode = xmllib.SubElement(tnode, "Field", {"Id": it_id, "Name":it_name,
            "Description":it_desc, "Unit":it_unit, "ChineseName":it_cname, "GrainSize": it_grain,
            "Default":it_default, "Min":it_min, "Max":it_max})
            xmllib.SubElement(fnode, "Type", {"Namespace":it_ns, "Href":it_type,"HrefUuid":self.GetTypeUuid(it_type, it_ns) })
    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        self.elements = {}
        self.outfiles = []
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个XML对象 """

        #创建Namespace element
        for ns in self.GetNamespaces():
            root = self.CreateRootNode(ns)
            node = self.CreateNamespaceNode(root, ns)
            for item in self.GetItemByNamespace(ns):
                if   item.item_type == "EnumData":    #枚举类型
                    #print "enum item"
                    self.CreateEnumDataItem(node, item.item_ns, item.item_val)
                elif item.item_type == "ArrayData":   #数组类型
                    #print "array"
                    self.CreateArrayDataItem(node, item.item_ns, item.item_val)
                elif item.item_type == "CompData":    #复合结构
                    self.CreateCompDataItem(node, item)
                elif item.item_type == "ModelMessage":  #模型消息
                    self.CreateModelMessageItem(node, item)
                elif item.item_type == "ModelEvent":
                    self.CreateModelMessageItem(node, item)
            self.elements[ns] = root
        
    def BuildEnd(self):
        """结束构建 写入XML文件 """
        for ns in self.elements:
            root = self.elements[ns]
            self.SaveNamespaceFile(ns, root)

    def GetFiles(self):
        return self.outfiles
