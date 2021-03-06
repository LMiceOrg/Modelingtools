#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel数据模型生成类
XLDataModelGenerator

驱动modelparser工作
"""
#from __init__ import *
import autotools
#print __init__.l_ns_name
import datamodel.exceldatamodel
import modelparser.excelparseradaptor
import builder.xmldatastructbuilder
import builder.xmlmodeldescbuilder

import builder.msvc2008builder
import builder.inimodelperfbuilder
import re
import os
import time

pglobal = re.compile(r'^0[^_]+[_](\w+)[.]xls\w*')
pother = re.compile(r'^([^_]+)[_]([^_]+)[_]([^.]+)[.]xls\w*')

class XLDataModelGenerator(object):
    def __init__(self):
        self.dt = datamodel.exceldatamodel.ExcelDataModel()

        self.proj_root = ""
        self.datastructs={}

    def GetModelFolder(self):
        return autotools.default_model_folder.encode('utf-8')

    def FindFileBySurfix(self, flist, folder, surfix, pattern):
        files = os.listdir(folder)
        for fi in files:
            #decode filename from gbk to unicode codeset
            if type(fi) == str:
                fi = fi.decode('gbk')
            name = folder + os.path.sep + fi
            if os.path.isdir(name):
                #recursion call
                self.FindFileBySurfix(flist, name, surfix, pattern)
            elif os.path.isfile(name):
                #match pattern
                if len(re.findall(pattern, fi)) == 0:
                    continue
                if len(re.findall('[0-9A-Za-z][_]', name)) == 0:
                    continue
                if name.find(u'参考') >= 0:
                    continue
                if name.find(u'CM') >= 0:
                    continue
                #match surfix
                for sfix in surfix:
                    if name[-len(sfix):] == sfix :
                        flist.append(name)
                        break

    #Get Excel files in folder                    
    def GetFileList(self, folder, surfixs=".xls,.xlsx", pattern='^[^~].*[.]xls\w*'):
        """ 遍历文件夹查找所有满足后缀的文件 """

        self.proj_root = folder

        surfix = surfixs.split(",")
        if type(folder) == str:
            folder = folder.decode('utf-8')
        p = os.path.abspath(folder)
        flist = []
        if os.path.isdir(p):
            self.FindFileBySurfix(flist, p, surfix, pattern)
        else:
            raise "folder param(%s) is not a real folder" % str(folder)
        utf8list=[]
        for it in flist:
            utf8list.append(it.encode('utf-8'))
        return utf8list

    #Check Excel file model type
    def CheckExcelFileModel(self, apath):
        ret=[]
        folder, name = os.path.split(apath);
        #check folder type
        h ,t = os.path.split(folder)
        #Namespace
        ns_key = t[:2]
        if ns_key == autotools.default_ns_key:
            #Global namespace
            ns=autotools.nslist[ns_key]
            ret.append(ns[1])
            #File type
            lv = pglobal.findall(name)
            if len(lv) == 1:
                ret.append( lv[0] )
                ret.append( lv[0] )
                ret.append( lv[0] )
        elif autotools.nslist.has_key(ns_key):
            #Other namespace
            ns=autotools.nslist[ns_key]
            ret.append(ns[1])
            #File type
            lv = pother.findall(name)
            if len(lv) ==1 and len(lv[0]) == 3:
                ret.append(lv[0][0])
                ret.append(lv[0][1])
                ret.append(lv[0][2])
        elif autotools.model_decl_key == name[:len(autotools.model_decl_key)]:
            #模型描述Excel
            ns = autotools.default_ns_name
            ret.append(ns)
            #File type
            ret.append(autotools.model_decl_key)
            ret.append("ModelDeclaration")
            ret.append("ModelDeclaration")
        else:
            #default namespace
            ns = autotools.nslist[autotools.default_ns_key]
            ret.append(ns[1])
            #File type
            lv = pother.findall(name)
            if len(lv) ==1 and len(lv[0]) == 3:
                ret.append(lv[0][0])
                ret.append(lv[0][1])
                ret.append(lv[0][2])
        #print t, len(ret)
        if len(ret) == 4:
            return ret

    def Parse(self, files):
        xlparser = modelparser.excelparseradaptor.ExcelParserAdaptor(autotools.nslist, autotools.dt_mapping, autotools.default_ns_name)
        xlparser.Parse(files, self.dt)

    #Build XML-style data struct
    def BuildDataStruct(self, tofolder):
        p = os.path.join(self.proj_root, tofolder)
        if not os.path.exists(p):
            os.makedirs(p)
        bd = builder.xmldatastructbuilder.XMLDataStructBuilder(self.dt, p)
        bd.BuildBegin()
        bd.Build()
        bd.BuildEnd()
        #cache datastructs
        self.datastructs = dict( bd.datastructs)
        return bd.GetFiles()

    #Build XML-style model description
    def BuildModelDesc(self, tofolder):
        #t1 = time.time()
        p = os.path.join(self.proj_root, tofolder)
        if not os.path.exists(p):
            os.makedirs(p)
        bd = builder.xmlmodeldescbuilder.XMLModelDescBuilder(self.dt, p)
        #set datastructs
        bd.datastructs = self.datastructs

        bd.BuildBegin()
        #t3 = time.time()
        bd.Build()
        #t4=time.time()
        bd.BuildEnd()
        #t2 = time.time()
        #print "Build Model Desc", t2-t1,t3-t1, t4-t3, t2-t4
        return bd.GetFiles()

    ##Build MSVC2008 project
    def BuildMsvc2008Solution(self, hfolder, mfolder):

        ##1.检查路径
        ph = os.path.join(self.proj_root, hfolder)
        if not os.path.exists(ph):
            os.makedirs(ph)
        pm = os.path.join( self.proj_root, mfolder)
        if not os.path.exists(pm):
            os.makedirs( pm )
        #t1 = time.time()

        ##2.生成C++代码
        bd = builder.msvc2008builder.Msvc2008Builder(self.dt, ph)
        bd.model_folder=pm
        if autotools.external_model_code_tools != "":
            bd.buildtools=autotools.external_model_code_tools
        #set datastructs
        bd.datastructs = self.datastructs

        bd.BuildBegin()
        bd.Build()
        bd.BuildEnd()
        #t2 = time.time()
        #print "Build 2008 solution:", t2-t1

        ##3.模型参数配置文件
        f = self.BuildModelParam(mfolder)

        flist = bd.GetFiles()
        return flist+f

    ## Build all models .ini configuration files
    def BuildModelParam(self, folder):
        """ 生成模型性能参数的配置文件 """
        ##1.检查路径
        pm = os.path.join( self.proj_root, folder)
        if not os.path.exists(pm):
            os.makedirs( pm )
        ##2.生成配置文件
        perfbd = builder.inimodelperfbuilder.IniModelPerfBuilder(self.dt, pm)
        perfbd.BuildBegin()
        perfbd.Build()
        perfbd.BuildEnd()
        ##3.返回配置文件
        flist = perfbd.GetFiles()
        return flist

    def GetDataModel(self):
        return self.dt

    def GetSources(self):
        return self.dt.GetSources()

    def GetProjectRoot(self):
        return self.proj_root

    def ClearProject(self):
        self.dt.itdict = {}

    #unit test
    def test(self):
        import time
        infolder = 'I:/dist3/20151229/model'
        tofolder = 'I:/work/build-qautotools-Desktop_Qt_5_3_MinGW_w64_32bit_MSYS2-Debug'
        t1 = time.clock()
        flist = self.GetFileList(infolder)
        t2 = time.clock()
        vlist = []
        for f in flist:
            rt = self.CheckExcelFileModel(f)
            if rt != None:
                vlist.append(f)
                #print f
        #step 3
        t3 = time.clock()
        afiles = ','.join(vlist)
        self.Parse(afiles)
        #print self.dt.GetItemByNamespace("NTSim_Comm")[0].item_type
        #step 4
        t4= time.clock()
        self.BuildDataStruct(tofolder)
        t5 = time.clock()
        print "GetFileList\t\t", t2-t1
        print "CheckExcelFileModel\t\t", t3-t2
        print "Parse\t\t", t4-t3
        print "BuildDataStruct\t\t", t5-t4
        print "total", t5-t1
