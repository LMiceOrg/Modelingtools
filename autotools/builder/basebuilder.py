#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" basebuilder
All build's base class
"""

import xml.etree.cElementTree as xmllib
import autotools
import os
import re
import hashlib as md5

pother = re.compile(r'^([^_]+)[_]([^_]+)[_]([^.]+)[.]xls\w*')

class BaseBuilder(object):
    def __init__(self, dt):
        self.dt = dt #DataModel
        self.name = ""
        self.outfiles = [] #the generated file list
        self.types = {} #namespace ->{ name --> {key --> value} }
        if os.path.isfile(autotools.simapp_dtfile):
            self.ImportXMLType(autotools.simapp_dtfile)

    def RefineFileName(self, name):
        " make sure file name is valid"
        reserved=".>,<:;/?'\"\\|`~@#$%^&*-+=(){}[]"
        for k in reserved:
            name = name.replace(k, '_')
        return name

    def SaveFile(self, ctx, name, refine=True):
        #Make sure path is valid, or makedir
        path, nm = os.path.split( os.path.abspath(name) )
        if not os.path.exists( path ):
            os.makedirs(path)

        #Convert file name to lower
        name = os.path.join(path, nm.lower() )

        ctx = str(ctx)
        #Refinement content (utf-8 encoding)
        if refine:
            ctx = self.RefineContext(ctx)

        #Convert to unicode
        ctx = ctx.decode('utf-8')



        #Write to file with default encoding and bom
        f=open(name, "w")
        f.write( autotools.default_bom )
        f.write( ctx.encode(autotools.default_encoding) )
        f.close()

        #append file name to outfiles
        self.outfiles.append(name)

    def SourceToProject(self, item):
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

    def RefineContext(self, x):
        """ 根据配置的命名空间映射关系，调整输出的内容 """
        refines=autotools.namespace_refine_mapping
        for ns in refines.keys():
            x = x.replace(ns, refines[ns])
        return x

    def PrettifyName(self, name):
        """ Convert name to string type and strip <return> in content """
        if type(name) not in (str, unicode):
            name = str(name)
        return name.strip().replace("\n", "")

    def GenerateUUIDByName(self, name, ns=None):
        """ Generate UUID """
        if ns != None:
            name = ns + "." + name
        s = md5.md5(md5.md5(name).hexdigest()).hexdigest()
        return "-".join( (s[:8],s[8:12], s[12:16], s[16:20],s[20:]) ).upper()

    def RefineNamespace(self, name, ns):
        if name == '':
            #debug
            #raise ValueError("name is empty")
            name = 'long'
        name = name.strip()
        ns = ns.strip()
        if ns == '':
            ns = autotools.g_ns_name #Global namespace name
        if autotools.dt_mapping.has_key(name):
            ns = autotools.dt_mapping[name][1]
            name = autotools.dt_mapping[name][0]
        if ns == autotools.g_ns_name:#Global namespace name
            if self.types.has_key(ns) and self.types[ns].has_key(name):
                pass
            else:
                ns = autotools.default_ns_name
        return name,ns

    def GetTypeUuid(self, name, ns=''):
        if name == '':
            #debug
            #raise ValueError("name is empty")
            name = 'long'
        if ns == '':
            ns = autotools.g_ns_name #Global namespace name
        if autotools.dt_mapping.has_key(name):
            ns = autotools.dt_mapping[name][1]
            name = autotools.dt_mapping[name][0]
        try:
            if self.types.has_key(ns) and self.types[ns].has_key(name):
                return self.types[ns][name]['Uuid']
            else:
                for ns in self.types:
                    if self.types[ns].has_key(name):
                        return self.types[ns][name]['Uuid']
            #else goto here
            return self.GenerateUUIDByName(name, ns)
        except:
            raise ValueError("Type[%s, %s] has not uuid" % (ns, name) )
        
    def ImportXMLType(self, xmlfile):
        et = xmllib.parse(xmlfile)
        #print et
        root = et.getroot()
        #Import element
        for inode in  et.findall("./Import"):
            #add namespace
            ns = inode.attrib['Name']
            if ns == 'AppSim':
                ns = autotools.g_ns_name
            if not self.types.has_key( ns ):
                self.types[ns] = {}
            for tnode in inode.findall("./Type"):
                value = dict(tnode.attrib)
                if value.has_key("{http://www.w3.org/2001/XMLSchema-instance}type"):
                    value["xsi:type"]= value["{http://www.w3.org/2001/XMLSchema-instance}type"]
                    value.pop("{http://www.w3.org/2001/XMLSchema-instance}type")
                value["Description"] = ""
                #print tnode.attrib, type(tnode.attrib) == dict
                key = tnode.attrib["Name"]

                #Description optional
                dnode = tnode.find("./Description")
                if dnode != None:
                    value["Description"] = dnode.text
                #Insert into namespace
                self.types[ns][key]=value
        #Namespace element
        for inode in et.findall("./Namespace"):
            #add namespace
            ns = inode.attrib['Name']
            if not self.types.has_key( ns ):
                self.types[ns] = {}
            for tnode in inode.findall("./Type"):
                key = tnode.attrib["Name"]
                value = dict(tnode.attrib)
                if value.has_key("{http://www.w3.org/2001/XMLSchema-instance}type"):
                    value["xsi:type"]= value["{http://www.w3.org/2001/XMLSchema-instance}type"]
                    value.pop("{http://www.w3.org/2001/XMLSchema-instance}type")
                if not value.has_key("Description"):
                    value["Description"] = ""
                #Description optional
                dnode = tnode.find("./Description")
                if dnode != None:
                    value["Description"] = dnode.text
                self.types[ns][key] = value
        # print self
        
    def BuildBegin(self, *args, **kw):
        #print "build begin", simapp_dtfile
        pass
    
    def Build(self, *args, **kw):
        pass

    def BuildEnd(self, *args, **kw):
        pass

    def GetFiles(self, *args, **kw):
        return list() #an empty list

    #helper methods
    def GetItems(self):
        return self.dt.GetItems()

    def GetNamespaces(self):
        return self.dt.GetNamespaces()

    def GetItemByNamespace(self, ns):
        return self.dt.GetItemByNamespace(ns)
