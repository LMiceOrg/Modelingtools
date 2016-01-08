#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel数据模型生成类
XLDataModelGenerator

驱动modelparser工作
"""
from __init__ import *
from datamodel.exceldatamodel import ExcelDataModel
from modelparser.excelpublicenumparser import ExcelPublicEnumParser
from modelparser.excelpubliccompparser import ExcelPublicCompParser
from modelparser.excelpublicarrayparser import ExcelPublicArrayParser
from modelparser.excelmodelpropertyparser import ExcelModelPropertyParser
from modelparser.excelmodelmessageparser import ExcelModelMessageParser
from modelparser.excelmodeleventparser import ExcelModelEventParser
from modelparser.excelmodelinitparamparser import ExcelModelInitParamParser

from builder.xmldatastructbuilder import XMLDataStructBuilder
from builder.xmlmodeldescbuilder import XMLModelDescBuilder
import re
import os
import xlrd

pglobal = re.compile(r'^0[^_]+[_](\w+)[.]xls\w*')
pother = re.compile(r'^([^_]+)[_]([^_]+)[_]([^.]+)[.]xls\w*')

class XLDataModelGenerator(object):
    def __init__(self):
        self.dt = ExcelDataModel()
        self.peparser = ExcelPublicEnumParser(nslist, dt_mapping, default_ns_name)
        self.pcparser = ExcelPublicCompParser(nslist, dt_mapping, default_ns_name)
        self.paparser = ExcelPublicArrayParser(nslist, dt_mapping, default_ns_name)
        self.mpparser = ExcelModelPropertyParser(nslist, dt_mapping, default_ns_name)
        self.mmparser = ExcelModelMessageParser(nslist, dt_mapping, default_ns_name)
        self.meparser = ExcelModelEventParser(nslist, dt_mapping, default_ns_name)
        self.miparser = ExcelModelInitParamParser(nslist, dt_mapping, default_ns_name)
    #Read Excel file content
    def GetExcelContent(self, name):
        #return {sheetindex: (sheetname, sheet UsedRange value) dict
        ctx = {}
        #if type(name) != unicode:
        #raise TypeError("name must be unicode")
        book = xlrd.open_workbook(name)
        if book == None:
            raise "Open Excel(%s) failed!" % name.encode('utf-8')
        for i in range(book.nsheets):
            s = book.sheet_by_index(i)
            sname = s.name
            svalue = list()
            for r in range(s.nrows):
                svalue.append( s.row_values(r) )
            ctx[i] = (sname, svalue)
        return ctx
        
    #Read Excel file content
    def GetExcelContent2(self, name, oApp=None):
        #return {sheetindex: (sheetname, sheet UsedRange value) dict
        import win32com.client
        ctx={}
        oxl = None
        #Create Excel OLE object
        if oApp == None:
            oxl = win32com.client.Dispatch("Excel.Application")
        else:
            oxl = oApp

        #Open Excel file
        rt = oxl.Workbooks.Open(name)
        if rt == False:
            raise "Open Excel(%s) failed!" %name
        cnt = oxl.ActiveWorkbook.Sheets.Count
        for i in range(cnt):
            sname = oxl.ActiveWorkbook.Sheets[i].Name
            svalue = oxl.ActiveWorkbook.Sheets[i].UsedRange.Value
            ctx[i] = (sname, svalue)
        #Close Excel file
        oxl.Workbooks.Close()
        if oApp == None:
            oxl = None

        return ctx

    def FindFileBySurfix(self, flist, folder, surfix):
        files = os.listdir(folder)
        for fi in files:
            #decode filename from gbk to unicode codeset
            if type(fi) == str:
                fi = fi.decode(dcs)
            name = folder + os.path.sep + fi
            if os.path.isdir(name):
                #recursion call
                self.FindFileBySurfix(flist, name, surfix)
            elif os.path.isfile(name):
                for sfix in surfix:
                    if name[-len(sfix):] == sfix :
                        flist.append(name)
                        break
    #Get Excel files in folder                    
    def GetFileList(self, folder, surfixs=".xls,.xlsx"):
        """ 遍历文件夹查找所有满足后缀的文件 """
        surfix = surfixs.split(",")
        if type(folder) == str:
            folder = folder.decode('utf-8')
        p = os.path.abspath(folder)
        flist = []
        if os.path.isdir(p):
            self.FindFileBySurfix(flist, p, surfix)
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

    # Parse Excel filelist
    def Parse(self, files):
        #print "parse files:", files.decode('utf-8').encode('gbk')
        #To unicode string
        flist = files.decode('utf-8').split(',')

        #Loop each Excel file in flist
        for xl_name in flist:
            if xl_name == '':
                continue
            
            ctx = self.GetExcelContent(xl_name)
            xlfile = os.path.split(xl_name)[1]

            #Public struct Excel style (检查规则：文件以0开头)
            if xlfile[0] == '0' :
                if xlfile.find('EnumDataType') >= 0:
                    #Loop each sheet by sheet index
                    for sh_idx in ctx:
                        sh_name, sh_ctx = ctx[sh_idx]
                        #print "parse Public Enum"
                        self.peparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    
                elif xlfile.find('CompDataType') >= 0:
                    #Loop each sheet by sheet index
                    for sh_idx in ctx:
                        sh_name, sh_ctx = ctx[sh_idx]
                        self.pcparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    
                elif xlfile.find('ArrayDataType') >= 0:
                    #Loop each sheet by sheet index
                    for sh_idx in ctx:
                        sh_name, sh_ctx = ctx[sh_idx]
                        self.paparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    
            else: #模型的数据结构定义文件 (初始化参数，输入输出消息，发送接收事件，性能属性)
                if len(ctx) >= 4:
                    #model init param
                    sh_idx = 0
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.miparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model message
                    sh_idx = 1
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.mmparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model event
                    sh_idx = 2
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.meparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model property
                    sh_idx = 3
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.mpparser.ParseExcelSheet(self.dt, xl_name, sh_ctx, sh_idx, sh_name)

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
