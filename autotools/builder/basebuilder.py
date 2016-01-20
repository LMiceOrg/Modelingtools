#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" basebuilder
建造者基类
"""

import xml.etree.cElementTree as xmllib
from autotools.__init__ import *

import os
import hashlib as md5

class BaseBuilder(object):
    def __init__(self, dt):
        self.dt = dt #DataModel
        self.name = ""
        self.types = {} #namespace ->{ name --> {key --> value} }
        if os.path.isfile(simapp_dtfile):
            self.ImportXMLType(simapp_dtfile)

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
        if ns == '':
            ns = g_ns_name #Global namespace name
        if dt_mapping.has_key(name):
            ns = dt_mapping[name][1]
            name = dt_mapping[name][0]
        if ns == g_ns_name:#Global namespace name
            if self.types.has_key(ns) and self.types[ns].has_key(name):
                pass
            else:
                ns = default_ns_name
        return name,ns

    def GetXsiType(self, name, ns=''):
        if ns == '':
            ns = g_ns_name #Global namespace name
        if dt_mapping.has_key(name):
            ns = dt_mapping[name][1]
            name = dt_mapping[name][0]
        try:
            if self.types.has_key(ns) and self.types[ns].has_key(name):
                return self.types[ns][name]['xsi:type'], name, ns
            elif name[:4] == "Enum":
                if ns == g_ns_name: #Global namespace name
                    ns = default_ns_name
                return "Types:Enumeration", name, ns
            else:
                if ns == g_ns_name: #Global namespace name
                    ns = default_ns_name
                return "Types:Structure", name, ns
        except:
            raise ValueError("Type[%s] has not uuid" % name)
    def GetTypeUuid(self, name, ns=''):
        if name == '':
            #debug
            #raise ValueError("name is empty")
            name = 'long'
        if ns == '':
            ns = g_ns_name #Global namespace name
        if dt_mapping.has_key(name):
            ns = dt_mapping[name][1]
            name = dt_mapping[name][0]
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
                ns = g_ns_name
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
