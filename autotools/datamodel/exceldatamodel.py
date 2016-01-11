#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ExcelDataModel
Excel数据模型
"""

import datamodel
import dataitem

class ExcelDataModel(datamodel.DataModel):
    def __init__(self):
        self.itdict = {}
        self.xldict = {}

    def CheckGrainItem(self, item):
        """ 规则: 复合数据结构中的多粒度参数解析 在列（粒度）的值为(1+), 其粒度数量是上一个字段
            其类型为string
        """
        if item.it_type in ("CompData", "ModelEvent", "ModelMessage"):
            if item.it_val[4].strip() == "1+":
                #variant-length sub-struct
                return True

        return False

    def AppendItem(self, xl_name, sh_idx, sh_name, namespace, it_type, it_val):
        """ 向数据模型中添加数据项
            xl_name: Excel文件名称
            pt_type: 数据项的类型
            sh_idx：表单索引
            sh_name：表单名称
            namespace：表单的名字空间
            it_val：数据项的值
        """
        item = dataitem.DataItem(xl_name, sh_idx, sh_name, namespace, it_type, it_val)
        if self.itdict.has_key(namespace):
            self.itdict[namespace].append(item)
        else:
            self.itdict[namespace] = [item]

        if self.xldict.has_key(xl_name):
            self.xldict[xl_name].append([sh_idx, sh_name])
        else:
            self.xldict[xl_name]=list([[sh_idx, sh_name]])

    def GetItems(self):
        return self.itdict.values()

    def GetNamespaces(self):
        return self.itdict.keys()
    
    def GetItemByNamespace(self, namespace):
        if self.itdict.has_key(namespace):
            return self.itdict[namespace]
        else:
            return list() #an empty list

    def GetSources(self):
        return self.xldict.keys()

    def GetParts(self):
        return self.xldict.values()

    def GetPartBySource(self, src):
        if self.xldict.has_key(src):
            return self.xldict[src]
        else:
            return list() #an empty part
