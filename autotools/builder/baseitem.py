#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BaseItem(object):
    """ BaseItem class"""
    def __init__(self, *arg, **kw):
        self.name_list=[]
        self.value_list = []
        if len(arg) >= 1 and type(arg[0]) in (tuple, list):
            nm_size = len(arg[0])
            self.name_list += arg[0][:]
            #has value list
            if len(arg) >=2 and type(arg[1]) in (tuple,list):
                vl_size = len(arg[1])
                sz = min(nm_size, vl_size)
                self.value_list += arg[0][:sz]
                self.value_list += ['']* (nm_size - sz)
            #no value list
            else:
                self.value_list += ['']*(len(arg[0]))
        if kw.has_key('name_list') and type(kw['name_list']) in (tuple, list):
            nm_size = len(kw['name_list'])
            self.name_list += kw['name_list'][:]
            #has value_list
            if kw.has_key('value_list') and type(kw['value_list']) in (tuple, list):
                vl_size = len(kw['value_list'])
                sz = min(nm_size, vl_size)
                self.value_list += kw['value_list'][:sz]
                self.value_list += [''] * (nm_size - sz)
                kw.pop('value_list')
            #no value_list
            else:
                self.value_list += [''] * nm_size
            kw.pop('name_list')
        for key in kw:
            #print key
            self.name_list.append(key)
            self.value_list.append(kw[key])
    #list method
    def __getitem__(self, idx):
        return self.value_list[idx]
    def __setitem__(self, idx, value):
        self.value_list[idx]=value
    def __len__(self):
        return len(self.value_list)
    #dict method
    def __getattr__(self, name):
        if self.name_list.count(name) > 0:
            return self.value_list[self.name_list.index(name)]
        else:
            # Default behaviour
            return object.__getattribute__(self, name)
    def __repr__(self):
        return "BaseItem " + str(zip(self.name_list, self.value_list)) + " at 0x%x" % id(self)
    @property
    def __dict__(self):
        return dict( zip(self.name_list, self.value_list) )
