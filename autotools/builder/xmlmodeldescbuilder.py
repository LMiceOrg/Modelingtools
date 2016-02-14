#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" XMLModelDescBuilder
XML格式的模型描述建造者
"""

import basebuilder
import autotools
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
            self.folder = os.path.abspath(folder)
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        
        self.outfiles = []
        self.datastructs = {}

    def GetModelDecl(self, pj_name):
        #print pj_name, self.projects.has_key(pj_name)
        if self.projects.has_key(pj_name):
            name = self.projects[pj_name][2]
            key = "%s_%s"% (self.projects[pj_name][1],name)
            if self.md_dict.has_key(key):
                return self.md_dict[key]
            elif self.md_dict.has_key(name):
                return self.md_dict[name]
        #print "no model decl"
        raise ValueError("Project(%s) does not has its model declaration" % pj_name)

    def GenerateProjectRootNode(self, pj_name):
        root = xmllib.Element("Component:Component_Define", {}, **autotools.l_xmlns_modeldescs)
        comment = xmllib.Comment("Edited with Modelingtools by LMice TEAM, generated by ElementTree(Python) at: %s " % time.ctime() )
        root.append(comment)

        #获得模型的描述信息
        md_item = self.GetModelDecl(pj_name)

        pnode = xmllib.SubElement(root, "Project", {"Id":md_item.item_val[6], "Name":md_item.item_val[6], "Language":"C++"})
        xmllib.SubElement(pnode, "Description").text = "%s; %s." % (md_item.item_val[4], md_item.item_val[5])
        return root

    def GetXsiType(self, name, ns=''):
        """ 根据类型的名称和命名空间， 生成xsi:type """
        #print name, ns
        if ns == '':
            ns = autotools.g_ns_name #Global namespace name
        if autotools.dt_mapping.has_key(name):
            ns = autotools.dt_mapping[name][1]
            name = autotools.dt_mapping[name][0]

        if self.types.has_key(ns) and self.types[ns].has_key(name): #已有类型
            return self.types[ns][name]['xsi:type'], name, ns
        else: #从自定义数据中查找
            node_id = "%s.%s" %(ns, name)
            if self.ds_nodes.has_key(node_id):
                return self.ds_nodes[node_id].get("xsi:type"), name, ns
        #print str(self.ds_nodes)
        emsg="%s Type[%s.%s] has not uuid" % (self.cur_proj[0].encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'))
        for key in self.ds_nodes.keys():
            if key.find(name) >= 0:
                same_key = key
                emsg = "%s Type[%s.%s] has not uuid, Do you mean[%s]" % (self.cur_proj[0].encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'), key.encode('utf-8'))
                break
        raise ValueError( emsg  )

    def GetXsiValueType(self, name, ns):
        """ 根据类型的名称和命名空间， 生成xsi:type """
        #print name, ns
        if ns == '':
            ns = autotools.g_ns_name #Global namespace name
        if autotools.dt_mapping.has_key(name):
            ns = autotools.dt_mapping[name][1]
            name = autotools.dt_mapping[name][0]

        if self.types.has_key(ns) and self.types[ns].has_key(name): #已有类型
            return "Types:%s" % name, name, ns
        else: #从自定义数据中查找
            node_id = "%s.%s" %(ns, name)
            if self.ds_nodes.has_key(node_id):
                return self.ds_nodes[node_id].get("xsi:type"), name, ns
        #print str(self.ds_nodes)
        emsg="%s Type[%s.%s] has not uuid" % (self.cur_proj[0].encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'))
        for key in self.ds_nodes.keys():
            if key.find(name) >= 0:
                same_key = key
                emsg = "%s Type[%s.%s] has not uuid, Do you mean[%s]" % (self.cur_proj[0].encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'), key.encode('utf-8'))
                break
        raise ValueError( emsg  )

    def ValidateName(self, name, ns):
        isValid = False
        name, ns = self.RefineNamespace(name, ns)
        node_id = "%s.%s" % (ns, name)
        if self.types.has_key(ns) and self.types[ns].has_key(name): #已有类型
            isValid = True #"Types:%s" % name, name, ns
        else: #从自定义数据中查找
            node_id = "%s.%s" %(ns, name)
            if self.ds_nodes.has_key(node_id):
                isValid = True #self.ds_nodes[node_id].get("xsi:type"), name, ns
        #print str(self.ds_nodes)
        if isValid:
            return node_id
        fname = os.path.split(self.cur_item.source)[1]
        emsg="%s[%s]:%s Type[%s.%s] has not uuid" % (self.cur_item.item_type.encode('utf-8'), self.cur_item.part_name.encode('utf-8'), fname.encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'))
        for key in self.ds_nodes.keys():
            if key.find(name) >= 0:
                same_key = key
                emsg = "%s[%s]:%s Type[%s.%s] has not uuid, Do you mean[%s]" % (self.cur_item.item_type.encode('utf-8'), self.cur_item.part_name.encode('utf-8'), fname.encode('utf-8'), ns.encode('utf-8'), name.encode('utf-8'), key.encode('utf-8'))
                break
        #raise ValueError( emsg  )
        self.errmsgs.append(emsg)

    def GetArrayElementTypeAndSize(self, name, ns):
        """ namespace, name, size """
        node_id = "%s.%s" %(ns, name)
        if self.ds_nodes.has_key(node_id):
            it = self.ds_nodes[node_id].find("ItemType")
            return it.get("Namespace"), it.get("Href"), self.ds_nodes[node_id].get("Size")
        else:
            if name.find("Wstring") == 0:
                ssz = name.replace("Wstring", "").strip()
                return ns, "Wchar", ssz
            elif name.find("String") == 0:
                ssz = name.replace("String", "").strip()
                return ns, "Char", ssz
    def GenerateProjectImport2(self, pj_name, root):
        """all """
        ids = self.ds_nodes.keys()
        ids.sort()
        last_ns = ""
        nsd=autotools.l_ns_name
        nsnode = xmllib.SubElement(root, "Import", {"Id":nsd, "Name":nsd, "Location":nsd})
        for id in ids:
            ns, nm = id.split(".")
            if last_ns != ns:
                last_ns = ns

            tnode = self.ds_nodes[id]
            nsnode.append(tnode)
        ids = self.types.keys()
        ids.sort()
        for ns in ids:
            if last_ns != ns:
                last_ns = ns
                nsnode = xmllib.SubElement(root, "Import", {"Id":ns, "Name":ns,"Location":ns})
            for nm in self.types[ns].keys():
                t = self.types[ns][nm]
                tnode = xmllib.SubElement(nsnode, "Type", {"Id": t["Id"], "Name":t["Name"],
                                                           "Uuid":t["Uuid"], "xsi:type":t["xsi:type"] })
                xmllib.SubElement(tnode, "Description").text=t["Description"]

    def RecursiveFindType(self, node_id, imports, lv):
        lv = lv -1
        if lv <= 0:
            return
        if self.depends.has_key(node_id):
            for key in self.depends[node_id]:
                if self.ds_nodes.has_key(key):
                    tnode = self.ds_nodes[key]
                    imports[key] = tnode
                    self.RecursiveFindType(node_id, imports, lv)

    def GenerateProjectImport(self, pj_name, root):

        #return self.GenerateProjectImport2(pj_name, root)

        if not self.reftypes.has_key(pj_name):
            return
        imports = {}
        tlist = self.reftypes[pj_name]

        for id in tlist:
            namespace, name = tlist[id]
            xsi_type,xsi_name,xsi_ns = self.GetXsiType(name, namespace)
            node_id = "%s.%s" %(xsi_ns, xsi_name)
            if self.ds_nodes.has_key(node_id):
                tnode = self.ds_nodes[node_id]
                imports[node_id] = tnode
                self.RecursiveFindType(node_id, imports, 5)

        nsnode = xmllib.SubElement(root, "Import", {"Id":'NTSim', "Name":'NTSim',
            "Location":'NTSim'})
        for key in imports:
            nsnode.append( imports[key] )

        ids = self.types.keys()
        ids.sort()
        last_ns = ''
        for ns in ids:
            if last_ns != ns:
                last_ns = ns
                nsnode = xmllib.SubElement(root, "Import", {"Id":ns, "Name":ns,"Location":ns})
            for nm in self.types[ns].keys():
                t = self.types[ns][nm]
                tnode = xmllib.SubElement(nsnode, "Type", {"Id": t["Id"], "Name":t["Name"],
                                                           "Uuid":t["Uuid"], "xsi:type":t["xsi:type"] })
                xmllib.SubElement(tnode, "Description").text=t["Description"]

        return
        for id in tlist:
            namespace, name = tlist[id]

            #name, namespace = self.RefineNamespace(name, namespace)
            if not imports.has_key(namespace):
                nsnode = xmllib.SubElement(root, "Import", {"Id":namespace, "Name":namespace,
                    "Location":namespace})
                imports[namespace] = nsnode
            nsnode = imports[namespace]
            xsi_type,xsi_name,xsi_ns = self.GetXsiType(name, namespace)
            node_id = "%s.%s" %(xsi_ns, xsi_name)
            if xsi_type == None:
                #print node_id, " has none xsi_type"
                raise ValueError("has none xsi_type")
            #nsnode = xmllib.SubElement(nsnode, "Type", {"Id":node_id,"Name":xsi_name,
            #    "Uuid":self.GetTypeUuid(xsi_name, xsi_ns), "xsi:type": xsi_type })
            if self.ds_nodes.has_key(node_id):
                tnode = self.ds_nodes[node_id]
                tnode.set("xsi:type", xsi_type)
            #if self.datastructs.has_key(node_id):
            #    ctx = self.datastructs[node_id].replace('xsi:type', 'xsi_type')
            #    tnode = xmllib.fromstring(ctx)
            #    if tnode.attrib.has_key('xsi_type'):
            #        tnode.attrib.pop('xsi_type')
            #
            #    tnode.set("xsi:type", xsi_type)
            #    #tnode.set("Uuid", self.GetTypeUuid(xsi_name, xsi_ns))
            #    #tnode.set("Id",node_id)
            #    #tnode.set("Name",xsi_name)

                nsnode.append(tnode)
        #Generate Global namespace import
        key = autotools.g_ns_name
        if imports.has_key(key):
            nsnode = imports[key]
            if self.types.has_key(key):
                for tp_name in self.types[key]:

                    xmllib.SubElement(nsnode, "Type", **self.types[key][tp_name])

    def GenerateComponentNode(self, pj_name, root):
        """生成组件节点 """

        #获得模型的描述信息
        md_item = self.GetModelDecl(pj_name)

        com = xmllib.SubElement(root, "Component", {"type":pj_name, "category":"ModelComponent",
            "GUID": "{%s}" % self.GetTypeUuid(pj_name, "Constructive"),
                                                     "LVC_Feature":"Constructive"})
        xmllib.SubElement(com, "Inherit")
        dnode = xmllib.SubElement(com, "Description")
        xmllib.SubElement(dnode, "ChineseName").text = md_item.item_val[4]
        xmllib.SubElement(dnode, "EnglishName").text = md_item.item_val[6]#DLL Name
        xmllib.SubElement(dnode, "Creator").text = md_item.item_val[7][9]
        xmllib.SubElement(dnode, "Department").text = autotools.l_ns_name
        xmllib.SubElement(dnode, "DdevelopDate").text = time.strftime("%Y-%m-%d %H:%M:%S")
        xmllib.SubElement(dnode, "Version").text = "V1.0"

        pj_element = self.elements[pj_name]
        if pj_element.has_key("Properties"):
            com.append(pj_element["Properties"])
        else:
            xmllib.SubElement(com, "Properties")

        if pj_element.has_key("Inputs"):
            com.append(pj_element["Inputs"])
        else:
            xmllib.SubElement(com, "Inputs")

        if pj_element.has_key("Outputs"):
            com.append(pj_element["Outputs"])
        else:
            xmllib.SubElement(com, "Outputs")

        if pj_element.has_key("ReceiveEvents"):
            com.append(pj_element["ReceiveEvents"])
        else:
            xmllib.SubElement(com, "ReceiveEvents")

        if pj_element.has_key("SendEvents"):
            com.append(pj_element["SendEvents"])
        else:
            xmllib.SubElement(com, "SendEvents")

    def GenerateCompositeNode(self, pj_name, root):
        return

    def GenerateResourceNode(self, pj_name, root):
        """ 生成资源节点 """

        #获得模型的描述信息
        md_item = self.GetModelDecl(pj_name)

        xmllib.SubElement(root, "Resource", {"platform":"_X86_32_WIN_5_VC90", "path":"", "name":"%s.dll" % md_item.item_val[6]})

    def SaveDscFile(self, pj_name, root):

        #获得模型的描述信息
        md_item = self.GetModelDecl(pj_name)
        md_name = md_item.item_val[6]
        if md_name.find('_') < 0:
            return

        x = xmllib.tostring(root, 'utf-8')
        # 将Excel中换行符替换为 空格
        x = x.replace('&#xd;', ' ').replace('\n', ' ')
        x = self.RefineContext(x)
        #doc = minidom.parseString( x )
        data = '<?xml version="1.0" encoding="utf-8"?>'+x
        #data = doc.toprettyxml(encoding="utf-8")
        name = os.path.join(self.folder, u"%s.xml" % md_item.item_val[6])

        f = open(name, "w")
        f.write(data)
        f.close()
        self.outfiles.append(name.encode('utf-8'))

    def ParseItemSource(self, item):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.SourceToProject(item)
        #store project properties
        self.projects[pj_name] = [item.source, pj_num, pj_name, pj_cname]
        self.cur_proj=self.projects[pj_name]
        return pj_num, pj_name, pj_cname

    def InitProjectNodes(self, pj_name):
        ids=["Properties", 'Inputs', 'Outputs', 'ReceiveEvents', 'SendEvents']
        self.elements[pj_name]={}
        for id in ids:
            self.elements[pj_name][id] = xmllib.Element(id)

    def GetProjectNodeByName(self, pj_name, key):
        if not self.elements.has_key(pj_name):
            self.InitProjectNodes(pj_name)

        if not self.elements[pj_name].has_key(key):
            node = xmllib.Element(key)
            self.elements[pj_name][key] = node
        return self.elements[pj_name][key]

    def CreateModelInitParamItem(self, data):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.ParseItemSource(data)
        if pj_num == "":
            return
        pps = self.GetProjectNodeByName(pj_name, "Properties")
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
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item[:10]
            pp = xmllib.SubElement(pps, "Property", {"Name":it_name, "ChineseName":it_cname})
            xmllib.SubElement(pp, "Description").text = it_desc.replace('\n', '')
            #refinement namespace
            it_type, it_ns = self.RefineNamespace(it_type, it_ns)
            ## 生成变长类型参数
            it_type, it_ns = self.GetTypeNameAndNamespace(it_type, it_ns)

            xmllib.SubElement(pp, "Type", {"Namespace":it_ns,"Href":it_type, "HrefUuid":self.GetTypeUuid(it_type, it_ns)})
            #TODO: what are xsi:types of user defined types
            it_xsitype, it_type, it_ns = self.GetXsiValueType(it_type, it_ns)
            if it_xsitype == "Types:Array":
                #array data init
                ad_ns, ad_name, ad_size = self.GetArrayElementTypeAndSize(it_type, it_ns)
                ad_xsitype, ad_name, ad_ns = self.GetXsiType(ad_name, ad_ns)
                dnode = xmllib.SubElement(pp, "Default", {"xsi:type":"%sValue" % it_xsitype})
                dnode.extend( [xmllib.Element("ItemValue", {"Value":"", "xsi:type":"Types:%sValue" % ad_name }) ] * int(ad_size) )
                #for i in range( int(ad_size) ):
                #    xmllib.SubElement(dnode, "ItemValue", {"Value":"", "xsi:type":"Types:%sValue" % ad_name })

            else:
                xmllib.SubElement(pp, "Default", {"Value":it_default, "xsi:type":"%sValue" % it_xsitype})

            #update reftypes
            if not self.reftypes.has_key(pj_name):
                self.reftypes[pj_name]={}
            self.reftypes[pj_name]["%s.%s" %(it_ns, it_type)] = [it_ns, it_type]

    def CreateModelMessageItem(self, item):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.ParseItemSource(item)
        if pj_num == "":
            return

        #Create in/out Message nodes
        innode =    self.GetProjectNodeByName(pj_name, "Inputs")
        outnode =   self.GetProjectNodeByName(pj_name, "Outputs")
        parent = innode
        name = "Input"
        cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cp_items = item.item_val[:7]
        cp_type = cp_name + "_T"
        cp_type, cp_ns = self.RefineNamespace(cp_type, cp_ns)
        ## 生成变长类型参数
        cp_type, cp_ns = self.GetTypeNameAndNamespace(cp_type, cp_ns)

        if cp_io == u"输出":
            parent = outnode
            name = "Output"
        onode = xmllib.SubElement(parent, name, {"Name":cp_name})

        xmllib.SubElement(onode, "Type", {"Href":"%s" % cp_type, "HrefUuid":self.GetTypeUuid(cp_type, cp_ns),
            "Namespace":cp_ns})

        #update reftypes
        if not self.reftypes.has_key(pj_name):
            self.reftypes[pj_name]={}
        self.reftypes[pj_name]["%s.%s" %(cp_ns, cp_type)] = [cp_ns, cp_type]
    
    def GetTypeNameAndNamespace(self, cp_type, cp_ns):
        ## 生成变长类型参数
        cp_id = "%s.%s" % (cp_ns, cp_type)
        if self.grainlist.has_key(cp_id):
            cp_type = "String"
            cp_ns   = ""
            cp_type, cp_ns = self.RefineNamespace(cp_type, cp_ns)
        return cp_type, cp_ns

    def CreateModelEventItem(self, item):
        #Get pj_name from xlfile
        pj_num, pj_name, pj_cname = self.ParseItemSource(item)
        if pj_num == "":
            return

        #Create in/out Event nodes
        innode =    self.GetProjectNodeByName(pj_name, "ReceiveEvents")
        outnode =   self.GetProjectNodeByName(pj_name, "SendEvents")

        parent = innode
        name = "ReceiveEvent"
        cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cp_items = item.item_val[:7]
        cp_type = cp_name + "_T"
        cp_type, cp_ns = self.RefineNamespace(cp_type, cp_ns)

        ## 生成变长类型参数
        cp_type, cp_ns = self.GetTypeNameAndNamespace(cp_type, cp_ns)


        if cp_io == u"输出":
            parent = outnode
            name = "SendEvent"

        onode = xmllib.SubElement(parent, name, {"Name":cp_name})
        xmllib.SubElement(onode, "Type", {"Href":"%s" % cp_type, "HrefUuid":self.GetTypeUuid(cp_type, cp_ns),
            "Namespace":cp_ns})

        #update reftypes
        if not self.reftypes.has_key(pj_name):
            self.reftypes[pj_name]={}
        self.reftypes[pj_name]["%s.%s" %(cp_ns, cp_type)] = [cp_ns, cp_type]


    def BuildModelDeclaration(self):
        """ 构造模型描述字典 """
        self.md_dict = {}
        for item in self.GetItemByNamespace(autotools.default_ns_name):
            if item.item_type == "ModelDeclaration": #模型描述
                #print str(item.item_val)
                md_name = item.item_val[6]
                self.md_dict[md_name] = item

    def CheckGrain(self, grain):
        if grain.strip() == "1+":
            return True
        return False


    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        #super(XMLModelDescBuilder, self).BuildBegin()

        if not os.path.isdir(self.folder):
            raise RuntimeError("folder(%s) is not exist!" % self.folder)
        
        self.projects = {} #key:project name, value list of project property
        self.elements = {} #key:project name, value dict of {node_type:node}
        self.reftypes={} # key: project name, value: list of tuple(namespace,name)
        self.outfiles = []
        self.ds_nodes = {} #key:node_id, value: xmlElement
        for node_id in self.datastructs:
            #
            ctx = self.datastructs[node_id].replace('xsi:type', 'xsi_type')
            tnode = xmllib.fromstring(ctx)
            if tnode.attrib.has_key('xsi_type'):
                tnode.set("xsi:type", tnode.get("xsi_type") )
                tnode.attrib.pop('xsi_type')
            self.ds_nodes[node_id] = tnode

        ##校验所有类型是否存在
        #错误信息列表
        self.errmsgs = []
        #数据多粒度列表
        self.grainlist={}   #key: node_id, value: bool grain
        #类型依赖关系表
        self.depends={} # key: node_id, value:list of node_id
        for ns in self.GetNamespaces():
            for item in self.GetItemByNamespace(ns):
                self.cur_item = item
                if   item.item_type == "ModelMessage":    #模型消息
                    cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cps = item.item_val
                    cp_name += "_T"
                    node_id = self.ValidateName(cp_name, cp_ns)
                    for cp in cps:
                        it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc, it_asign = cp
                        dp_id = self.ValidateName(it_type, it_ns)
                        if not self.depends.has_key(node_id):
                            self.depends[node_id] = []
                        self.depends[node_id].append( dp_id )
                        if self.CheckGrain(it_grain):
                            self.grainlist[node_id] = True
                elif item.item_type == "ModelInitParam":    #模型参数
                    mp_name, mp_cname, mp_items = item.item_val
                    for cp in mp_items:
                        it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = cp
                        self.ValidateName(it_type, it_ns)
                elif item.item_type == "ModelEvent":    #模型事件
                    cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, cps = item.item_val
                    cp_name += "_T"
                    node_id = self.ValidateName(cp_name, cp_ns)
                    for cp in cps:
                        it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc, it_asign = cp
                        dp_id = self.ValidateName(it_type, it_ns)
                        if not self.depends.has_key(node_id):
                            self.depends[node_id] = []
                        self.depends[node_id].append(dp_id)
                        if self.CheckGrain(it_grain):
                            self.grainlist[node_id] = True
                elif item.item_type == "EnumData":  # 枚举类型
                    ed_type, ed_desc, ed_items = item.item_val
                elif item.item_type == "CompData":  #复合数据结构
                    cp_name, cp_desc, cps = item.item_val
                    node_id = self.ValidateName(cp_name, item.item_ns)
                    for cp in cps:
                        it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = cp
                        dp_id = self.ValidateName(it_type, it_ns)
                        if not self.depends.has_key(node_id):
                            self.depends[node_id] = []
                        self.depends[node_id].append(dp_id)
                        if self.CheckGrain(it_grain):
                            self.grainlist[node_id] = True
                elif item.item_type == "ArrayData": #数据类型
                    ad_ns = item.item_ns
                    ctx =   item.item_val
                    ad_name, it_ns, it_type, it_num, it_unit, ad_desc = ctx[:6]
                    ad_id = "%s.%s" %(ad_ns, ad_name)
                    node_id =           self.ValidateName(ad_name, ad_ns)
                    it_type, it_ns =    self.RefineNamespace(it_type, it_ns)
                    dp_id =             self.ValidateName(it_type, it_ns)
                    print ad_id, dp_id
                    if not self.depends.has_key(node_id):
                        self.depends[node_id] = []
                    self.depends[node_id].append(dp_id)
        if len(self.errmsgs) > 0:
            raise ValueError("\n".join(self.errmsgs) )

        ##检查模型数据是否为多粒度
        for node_id in self.depends.keys():
            if self.grainlist.has_key(node_id):
                continue
            flag = False
            for id_lv2 in self.depends[node_id]:
                if self.grainlist.has_key(id_lv2):
                    self.grainlist[node_id] = True
                    flag = True
                    break
                if not self.depends.has_key(id_lv2):
                    continue
                for id_lv3 in self.depends[id_lv2]:
                    if self.grainlist.has_key(id_lv3):
                        self.grainlist[node_id] = True
                        flag = True
                        break
                    if not self.depends.has_key(id_lv3):
                        continue
                    for id_lv4 in self.depends[id_lv3]:
                        if self.grainlist.has_key(id_lv4):
                            self.grainlist[node_id] = True
                            flag = True
                            break
                    if flag == True:
                        break
                if flag == True:
                    break


    def Build(self):
        """开始构建 为每一个ModelInitParam创建一个XML对象 """

        #首先构造模型描述字典 model_name --> model_declaration
        self.BuildModelDeclaration()

        for ns in self.GetNamespaces():
            for item in self.GetItemByNamespace(ns):
                if   item.item_type == "ModelMessage":    #模型消息
                    self.CreateModelMessageItem(item)
                elif item.item_type == "ModelInitParam":    #模型参数
                    self.CreateModelInitParamItem(item)
                elif item.item_type == "ModelEvent":    #模型事件
                    self.CreateModelEventItem(item)
                elif item.item_type == "EnumData":  # 枚举类型
                    #self.AddEnumType(item)
                    pass
                elif item.item_type == "CompData":  #复合数据结构
                    #self.AddCompType(item)
                    #print "CompData"
                    pass
                elif item.item_type == "ArrayData": #数据类型
                    #self.AddArrayType(item)
                    #print "ArrayData"
                    pass
    def BuildEnd(self):
        """写入 dsc文件 """
        #for k in self.ds_nodes.keys():
        #    print k
        #print 'default_ns_name:', len(self.GetItemByNamespace(autotools.default_ns_name) )
        for pj_name in self.elements:
            self.cur_proj = self.projects[pj_name]
            #create root node
            root = self.GenerateProjectRootNode(pj_name)
            #create import node
            self.GenerateProjectImport(pj_name, root)
            #create component node
            self.GenerateComponentNode(pj_name, root)
            #create composite node
            self.GenerateCompositeNode(pj_name, root)
            #create resource node
            self.GenerateResourceNode(pj_name, root)

            #save to dsc file
            if root == None:
                #print "none xml", pj_name
                pass
            else:
                self.SaveDscFile(pj_name, root)

    def GetFiles(self):
        return self.outfiles
