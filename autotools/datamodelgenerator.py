#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel数据模型生成类
XLDataModelGenerator

驱动modelparser工作
"""
from __init__ import *
from datamodel.exceldatamodel import ExcelDataModel
import modelparser.excelparseradaptor
from builder.xmldatastructbuilder import XMLDataStructBuilder
from builder.xmlmodeldescbuilder import XMLModelDescBuilder
import re
import os

pglobal = re.compile(r'^0[^_]+[_](\w+)[.]xls\w*')
pother = re.compile(r'^([^_]+)[_]([^_]+)[_]([^.]+)[.]xls\w*')

class XLDataModelGenerator(object):
    def __init__(self):
        self.dt = ExcelDataModel()
        self.xlparser = modelparser.excelparseradaptor.ExcelParserAdaptor(nslist, dt_mapping, default_ns_name)


    def FindFileBySurfix(self, flist, folder, surfix, pattern):
        files = os.listdir(folder)
        for fi in files:
            #decode filename from gbk to unicode codeset
            if type(fi) == str:
                fi = fi.decode(dcs)
            name = folder + os.path.sep + fi
            if os.path.isdir(name):
                #recursion call
                self.FindFileBySurfix(flist, name, surfix, pattern)
            elif os.path.isfile(name):
                #match pattern
                if len(re.findall(pattern, fi)) == 0:
                    continue
                #match surfix
                for sfix in surfix:
                    if name[-len(sfix):] == sfix :
                        flist.append(name)
                        break

    #Get Excel files in folder                    
    def GetFileList(self, folder, surfixs=".xls,.xlsx", pattern='^[^~].*[.]xls\w*'):
        """ 遍历文件夹查找所有满足后缀的文件 """
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
        if ns_key == default_ns_key:
            #Global namespace
            ns=nslist[ns_key]
            ret.append(ns[1])
            #File type
            lv = pglobal.findall(name)
            if len(lv) == 1:
                ret.append( lv[0] )
                ret.append( lv[0] )
                ret.append( lv[0] )
        elif nslist.has_key(ns_key):
            #Other namespace
            ns=nslist[ns_key]
            ret.append(ns[1])
            #File type
            lv = pother.findall(name)
            if len(lv) ==1 and len(lv[0]) == 3:
                ret.append(lv[0][0])
                ret.append(lv[0][1])
                ret.append(lv[0][2])
        else:
            #default namespace
            ns = nslist[default_ns_key]
            ret.append(ns[1])
            #File type
            lv = pother.findall(name)
            if len(lv) ==1 and len(lv[0]) == 3:
                ret.append(lv[0][0])
                ret.append(lv[0][1])
                ret.append(lv[0][2])
        if len(ret) == 4:
            return ret

    def Parse(self, files):
        self.xlparser.Parse(files, self.dt)

    #Build XML-style data struct
    def BuildDataStruct(self, tofolder):
        builder = XMLDataStructBuilder(self.dt, tofolder)
        builder.BuildBegin()
        builder.Build()
        builder.BuildEnd()
        return builder.GetFiles()

    #Build XML-style model description
    def BuildModelDesc(self, tofolder):
        builder = XMLModelDescBuilder(self.dt, tofolder)
        builder.BuildBegin()
        builder.Build()
        builder.BuildEnd()
        return builder.GetFiles()
    def GetDataModel(self):
        return self.dt

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
