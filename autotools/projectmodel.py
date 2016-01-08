#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib as md5
import xml.etree.cElementTree as xmllib
from __init__ import *


class BaseContext(dict):
    #Customizing attribute access 'obj.name'
    def __getattr__(self, name):
        name = name.lower()
        if self.has_key(name):
            return self[name]
        else:
            raise AttributeError("The [%s] is not a valid attribute" % name)
    def __setattr__(self, name, value):
        name = name.lower()
        self.__setitem__(name, value)
    def __missing__(self, key):
        lkey = key.lower()
        if self.has_key(lkey):
            return self[lkey]
        else:
            print "Missing key[%s]." % key
            return ""

class DataType(BaseContext):
    """DataType represent: ns -> {name -> id uuid, type, Description}"""
    def GenerateUUIDByName(self, name, ns=None):
        """ Generate UUID """
        if ns != None:
            name = ns + "." + name
        s = md5.md5(md5.md5(name).hexdigest()).hexdigest()
        return "-".join( (s[:8],s[8:12], s[12:16], s[16:20],s[20:]) ).upper()
    def GetUuid(self, ns, name):
        if ns == '':
            ns = 'AppSim'
        if dt_mapping.has_key(name):
            ns = dt_mapping[name][1]
            name = dt_mapping[name][0]
        try:
            if self.has_key(ns):
                return self[ns][name]['Uuid']
            else:
                return self.GenerateUUIDByName(name, ns)
        except:
            return self.GenerateUUIDByName(name, ns)
    def ImportXML(self, xmlfile):
        et = xmllib.parse(xmlfile)
        #print et
        root = et.getroot()
        #print "root node:", root.tag
        for inode in  et.findall("./Import"):
            #add namespace
            ns = inode.attrib['Name']
            if not self.has_key( ns ):
                self[ns] = {}
            for tnode in inode.findall("./Type"):
                value = dict(tnode.attrib)
                if value.has_key("{http://www.w3.org/2001/XMLSchema-instance}type"):
                    value["xsi:type"]= value["{http://www.w3.org/2001/XMLSchema-instance}type"]
                value["Description"] = ""
                #print tnode.attrib, type(tnode.attrib) == dict
                key = tnode.attrib["Name"]

                #Description optional
                dnode = tnode.find("./Description")
                if dnode != None:
                    value["Description"] = dnode.text
                #Insert into namespace
                self[ns][key]=value
        for inode in et.findall("./Namespace"):
            #add namespace
            ns = inode.attrib['Name']
            if not self.has_key( ns ):
                self[ns] = {}
            for tnode in inode.findall("./Type"):
                key = tnode.attrib["Name"]
                value = dict(tnode.attrib)
                if value.has_key("{http://www.w3.org/2001/XMLSchema-instance}type"):
                    value["xsi:type"]= value["{http://www.w3.org/2001/XMLSchema-instance}type"]
                if not value.has_key("Description"):
                    value["Description"] = ""
                #Description optional
                dnode = tnode.find("./Description")
                if dnode != None:
                    value["Description"] = dnode.text
                self[ns][key] = value
        # print self
class ProjectModel(BaseContext):
    def __init__(self, load_from_xml=None):
        if load_from_xml != None:
            LoadProjectModel(self, load_from_xml)
    def LoadProjectModel(self, xmlfile):
        pass
