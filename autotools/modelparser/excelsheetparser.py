#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel表单解析器基类
ExcelSheetParser
"""
import os

class ExcelSheetParser:
    def __init__(self, nslist, dt_mapping, default_ns):
        self.ns = ""
        self.nslist = nslist
        self.dt_mapping = dt_mapping
        self.default_ns = default_ns

    def strip(self, *args):
        """去除字符串两边的空格"""
        arglist = []
        if len(args) == 1 and type(args) in (tuple, list):
            args = args[0]
        for k in args:
            if type(k) == str:
                arg = k.decode('gbk').strip()
            elif type(k) == unicode:
                arg = k.strip()
            else:
                arg = k
            arglist.append(arg)
        return arglist

    def VerifyNsName(self, ns, name):
        if self.dt_mapping.has_key(name):
            ns = self.dt_mapping[name][1]
            name = self.dt_mapping[name][0]
        elif ns == '' or ns == None:
            ns = self.default_ns
        return ns,name
    
    def GetNsKeyBySheetName(self, name):
        for k in self.nslist:
            if name.find(self.nslist[k][0]) >= 0:
                return k
            
    def GetXmlElementByPublicSheetName(self, name):
        #print self.nslist
        nskey = self.GetNsKeyBySheetName(name.encode('utf-8'))
        if nskey == None:
            raise ValueError(u"Public Sheet(%s) is invalid" % name)
            return
        nsvalue = self.nslist[nskey]
        self.ns = nsvalue[1]
        
    def GetXmlElementByCustomExcelName(self, name):
        key = name[0] + '_'
        if self.nslist.has_key(key):
            nsvalue = self.nslist[key]
            self.ns = nsvalue[1]
        else:
            self.ns = self.default_ns
            
    def GetNamespace(self, xl_name, sh_idx, sh_name):
        """ 规则1： 0开头的Excel文件为公共定义文件,此时根据表单名称解析
            规则2：非0开头的Excel文件，根据文件名称解析
            规则3：不在nslist范围内的文件，使用默认命名空间”
        """
        if type(xl_name) <> unicode:
            raise "%s parse failed" % str(xl_name)
        xlfile = os.path.split(xl_name)[1]
        if xlfile[0] == '0':
            self.GetXmlElementByPublicSheetName(sh_name)
        else:
            self.GetXmlElementByCustomExcelName(xlfile)
        return self.ns
    
    def ParseExcelSheet(self, *args, **kw):
        pass
    
    
