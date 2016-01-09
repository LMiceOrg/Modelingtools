#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xlrd

import excelpublicenumparser
import excelpubliccompparser
import excelpublicarrayparser
import excelmodelpropertyparser
import excelmodelmessageparser
import excelmodeleventparser
import excelmodelinitparamparser


class ExcelParserAdaptor(object):
    def __init__(self, nslist, name_aliase, default_namespace):
        self.peparser = excelpublicenumparser.ExcelPublicEnumParser(nslist, name_aliase, default_namespace)
        self.pcparser = excelpubliccompparser.ExcelPublicCompParser(nslist, name_aliase, default_namespace)
        self.paparser = excelpublicarrayparser.ExcelPublicArrayParser(nslist, name_aliase, default_namespace)
        self.mpparser = excelmodelpropertyparser.ExcelModelPropertyParser(nslist, name_aliase, default_namespace)
        self.mmparser = excelmodelmessageparser.ExcelModelMessageParser(nslist, name_aliase, default_namespace)
        self.meparser = excelmodeleventparser.ExcelModelEventParser(nslist, name_aliase, default_namespace)
        self.miparser = excelmodelinitparamparser.ExcelModelInitParamParser(nslist, name_aliase, default_namespace)


    #Read Excel file content
    def GetExcelContent(self, name):
        """ 读取 Excel 文件内容 """
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
        """ COM模式读取Excel内容 """
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

    # Parse Excel filelist
    def Parse(self, files, dt):
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
                        self.peparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)

                elif xlfile.find('CompDataType') >= 0:
                    #Loop each sheet by sheet index
                    for sh_idx in ctx:
                        sh_name, sh_ctx = ctx[sh_idx]
                        self.pcparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)

                elif xlfile.find('ArrayDataType') >= 0:
                    #Loop each sheet by sheet index
                    for sh_idx in ctx:
                        sh_name, sh_ctx = ctx[sh_idx]
                        self.paparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)

            else: #模型的数据结构定义文件 (初始化参数，输入输出消息，发送接收事件，性能属性)
                if len(ctx) >= 4:
                    #model init param
                    sh_idx = 0
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.miparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model message
                    sh_idx = 1
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.mmparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model event
                    sh_idx = 2
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.meparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)
                    #model property
                    sh_idx = 3
                    sh_name, sh_ctx = ctx[sh_idx]
                    self.mpparser.ParseExcelSheet(dt, xl_name, sh_ctx, sh_idx, sh_name)

