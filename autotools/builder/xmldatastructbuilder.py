#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" XMLDataStructBuilder
XML格式的数据结构建造者
"""

import basebuilder
import autotools
import re
import os
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

#Array<Char,32>
adtype_parser = re.compile("^\s*Array[<]\s*(\w+)\s*[,]\s*(\w+)\s*[>]")

class XMLDataStructBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(XMLDataStructBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = os.path.abspath(folder)
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        
        self.outfiles = []
        #print self.folder
        
    def SaveNamespaceFile(self, ns, root):
        doc = minidom.parseString( xmllib.tostring(root, 'utf-8') )
        x = doc.toprettyxml(encoding="utf-8")
        name = os.path.join(self.folder, u"%s.xml" % ns)
        self.SaveFile(x, name)

    def SaveInAll(self):

        name = os.path.join(self.folder, u"%s.xml" % autotools.l_ns_name)
        if self.outfiles.count(name) >0 :
            return

        root = None
        nsnode = None
        for ns in self.elements:
            if root == None:
                root = self.elements[ns]
                nsnode = root.findall("./Namespace")[0]
            else:
                for inode in self.elements[ns].findall("./Namespace"):
                    for tnode in inode.findall("./Type"):
                        nsnode.append(tnode)
        if root == None:
            return

        doc = minidom.parseString( xmllib.tostring(root, 'utf-8') )
        x = doc.toprettyxml(encoding="utf-8")

        self.SaveFile(x, name)

    def CreateNamespaceNode(self, root, ns):
        """ 命名空间接点对象, 如果不存在则新建"""
        
        node = xmllib.SubElement(root, "Namespace", {"Id":ns, "Name":ns})
        xmllib.SubElement(node, "Description").text = "It is the data type definition of namespace named %s ." % ns
        return node

    def CreateRootNode(self,ns):
        """ 新建根接点 """
        root = xmllib.Element("Catalogue:Catalogue", {"Id":"%sDataType" % self.name,
                                                      "Name":"%sDataType" % self.name,
                                                      }, **autotools.l_xmlns_datastructs)
        xmllib.SubElement(root, "Description").text = "It is the definition file of namespace named %s." % ns
        xmllib.SubElement(root, "Import", {"Namespace":"%s" % autotools.g_ns_name, "Location":"%s" %  autotools.g_ns_name})
        return root

    def CreateEnumDataItem(self, node, data):
        """ 生成枚举类型 """
        ed_ns = data.item_ns
        ctx = data.item_val
        ed_type, ed_desc, ed_items = ctx[:3]
        ed_id = "%s.%s" %(ed_ns, ed_type)
        tnode = xmllib.Element("Type", {"Id": ed_id,"Name":ed_type,
                                         "Uuid": self.GetTypeUuid(ed_type, ed_ns),
                                         "xsi:type":"Types:Enumeration"
                                         } )
        xmllib.SubElement(tnode, "Description").text = ed_desc
        #xmllib.SubElement(tnode, "Source").text = "%s[%s]" %(data.source, data.part_name)
        for item in ed_items:
            it_name, it_value, it_desc = item[:3]
            it_id = "%s.%s" %(ed_id, it_name)
            inode = xmllib.SubElement(tnode, "Literal", {"Id":it_id,"Name":it_name,
                                                "Value":str(int( it_value ) ) })
            xmllib.SubElement(inode, "Description").text = it_desc
        node.append(tnode)
        #cache type node
        self.datastructs[ed_id] = xmllib.tostring(tnode)

    def ParseArrayDataType(self, ad_type):
        """ 解析ad_type 返回数据类型和数量"""
        items = adtype_parser.findall(ad_type)
        if len(items) == 0:
            raise ValueError("Array data type[%s] is invalid!" % ad_type)
        return items[0]

    def CreateArrayDataItem(self, node, ad_ns, ctx):
        """ 生成数组类型 """
        #print "array"
        ad_name, it_ns, it_type, it_num, it_unit, ad_desc = ctx[:6]
        ad_id = "%s.%s" %(ad_ns, ad_name)

        #it_type, it_num = self.ParseArrayDataType(ad_type)
        #it_ns = ''
        it_type, it_ns = self.RefineNamespace(it_type, it_ns)

        tnode = xmllib.Element("Type", {"Id":ad_id,
            "Uuid":self.GetTypeUuid(ad_name, ad_ns),
            "Name":ad_name,
            #"Dim":self.PrettifyName(ad_dim),
            "xsi:type":"Types:Array",
            "Size":it_num
            } )

        xmllib.SubElement(tnode, "Description").text = ad_desc
        xmllib.SubElement(tnode, "ItemType", {"Namespace":it_ns,
            "Href":it_type,
            "HrefUuid":self.GetTypeUuid(it_type, it_ns),
            "Dimension":it_unit })

        node.append(tnode)
        #cache type node
        self.datastructs[ad_id] = xmllib.tostring(tnode)

    def CreateCompDataItem(self, node, data):
        """ 生成复合结构体类型 """

        cp_ns = data.item_ns
        ctx = data.item_val
        cp_name, cp_desc, cp_items = ctx[:3]
        #print cp_name, cp_ns
        cp_id = "%s.%s" %(cp_ns, cp_name)
        #print type(data.part_name)
        tnode = xmllib.Element("Type", {"Id": cp_id,"Name":cp_name,
                                         "Uuid": self.GetTypeUuid(cp_name, cp_ns),
                                         "xsi:type":"Types:Structure"
                                         } )
        #xmllib.SubElement(tnode, "Description").text = "%s Source:%s[%s]" %(cp_desc, data.source, data.part_name)
        #xmllib.SubElement(tnode, "Source").text = "%s[%s]" %(data.source, data.part_name)
        xmllib.SubElement(tnode, "Description").text = cp_desc
        for item in cp_items:
            for i in range(len(item)):
                if item[i] == None:
                    item[i] = ""
                if type(item[i]) not in (str, unicode):
                    #print type(item[i]), type(item[i]) != unicode
                    item[i] = str(item[i])
            #it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc
            #print len(item)
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item[:10]
            #refinement namespace
            it_type, it_ns = self.RefineNamespace(it_type, it_ns)
            it_id = "%s.%s" %(cp_id, it_name)
            fnode = xmllib.SubElement(tnode, "Field", {"Id": it_id, "Name":it_name})
            #xmllib.SubElement(fnode, "Description").text = "%s %s" % (it_desc, str({"Unit":it_unit, "ChineseName":it_cname, "GrainSize": it_grain,
            #"Default":it_default, "Min":it_min, "Max":it_max} ))
            xmllib.SubElement(fnode, "Description").text = "%s :%s" % (it_desc, it_cname)
            xmllib.SubElement(fnode, "Type", {"Namespace":it_ns, "Href":it_type,
                "HrefUuid":self.GetTypeUuid(it_type, it_ns)
                ,"Dimension":it_unit
                })

        node.append(tnode)
        #cache type node
        self.datastructs[cp_id] = xmllib.tostring(tnode)

    def CreateModelMessageItem(self, node, data):
        """ 模型消息"""
        ctx = data.item_val
        cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cp_items = ctx[:7]

        cp_name += "_T"
        cp_id = "%s.%s" %(cp_ns, cp_name)

        if len(cp_items) == 1:
            if cp_items[0][0] == "":
                return
        
        #print type(data.part_name)
        tnode = xmllib.Element("Type", {"Id": cp_id,"Name":cp_name,
                                         "Uuid": self.GetTypeUuid(cp_name, cp_ns),
                                         "xsi:type":"Types:Structure" } )
        #xmllib.SubElement(tnode, "Description").text = "%s  %s[%s]" %(cp_cname, data.source, data.part_name)
        xmllib.SubElement(tnode, "Description").text = cp_cname
        #xmllib.SubElement(tnode, "Source").text = "%s[%s]" %(data.source, data.part_name)
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
            fnode = xmllib.SubElement(tnode, "Field", {"Id": it_id, "Name":it_name})

            #xmllib.SubElement(fnode, "Description").text = "%s %s" %( it_desc, str({"Unit":it_unit, "ChineseName":it_cname, "GrainSize": it_grain,
            #"Default":it_default, "Min":it_min, "Max":it_max}) )
            xmllib.SubElement(fnode, "Description").text = "%s %s" %( it_desc,it_cname)
            xmllib.SubElement(fnode, "Type", {"Namespace":it_ns, "Href":it_type,
                "HrefUuid":self.GetTypeUuid(it_type, it_ns)
                ,"Dimension":it_unit
                })

        node.append(tnode)
        #cache type node
        self.datastructs[cp_id] = xmllib.tostring(tnode)

    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        #数据结构定义需要在模型描述中复用，因此需要存储下来
        self.datastructs={} # id<ns::name> --> string<xml>
        self.elements = {}
        self.outfiles = []
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个XML对象 """
        #获取模型描述列表
        #创建Namespace element
        for ns in self.GetNamespaces():
            #print ns, len(self.GetItemByNamespace(ns))
            root = self.CreateRootNode(ns)
            node = self.CreateNamespaceNode(root, ns)
            for item in self.GetItemByNamespace(ns):
                if   item.item_type == "EnumData":    #枚举类型
                    #print "enum item"
                    self.CreateEnumDataItem(node, item)
                elif item.item_type == "ArrayData":   #数组类型
                    #print "array"
                    self.CreateArrayDataItem(node, item.item_ns, item.item_val)
                elif item.item_type == "CompData":    #复合结构
                    #print "CompData"
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
        self.SaveInAll()

    def GetFiles(self):
        outfiles = []
        for f in self.outfiles:
            outfiles.append( f.encode('utf-8') )
        return outfiles
