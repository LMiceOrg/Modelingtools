#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DataModel
数据模型基类

items -> list
namespaces -> list
itembynamespace -> list
"""

class DataModel(object):
    def __init__(self):
        pass
    
    def AppendItem(self, *args, **kw):
        pass
    
    def GetItems(self, *args, **kw):
        return list()

    def GetNamespaces(self, *args, **kw):
        return list()

    def GetItemByNamespace(self, *args, **kw):
        return list()
