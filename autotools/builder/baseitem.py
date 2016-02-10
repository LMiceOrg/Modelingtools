#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BaseItem(object):
    """ BaseItem class"""
    def __init__(self, *arg, **kw):
        self.append(*arg, **kw)

    def __len__(self):
        return len(self.__dict__.keys())

    def __repr__(self):
        return "BaseItem " + str(self.__dict__) + " at 0x%x" % id(self)
#    @property
#    def __dict__(self):
#        return dict( zip(self.name_list, self.value_list) )
    def dict(self):
        return self.__dict__
    def append(self, *arg, **kw):
        if len(arg) >= 1 and type(arg[0]) in (tuple, list):
            nm_size = len(arg[0])
            #self.name_list += arg[0][:]
            #has value list
            if len(arg) >=2 and type(arg[1]) in (tuple,list):
                vl_size = len(arg[1])
                sz = min(nm_size, vl_size)
                for i in range(sz):
                    key = arg[0][i]
                    val = arg[1][i]
                    self.__dict__[key] = val
                #self.value_list += arg[0][:sz]
                #self.value_list += ['']* (nm_size - sz)
                for i in range(nm_size - sz):
                    key = arg[0][sz+i]
                    val = ''
                    self.__dict__[key] = val
            #no value list
            else:
                #self.value_list += ['']*(len(arg[0]))
                for i in range(nm_size):
                    key = arg[0][i]
                    val = ''
                    self.__dict__[key]=val
        if kw.has_key('name_list') and type(kw['name_list']) in (tuple, list):
            nm_size = len(kw['name_list'])
            #self.name_list += kw['name_list'][:]
            #has value_list
            if kw.has_key('value_list') and type(kw['value_list']) in (tuple, list):
                vl_size = len(kw['value_list'])
                sz = min(nm_size, vl_size)
                for i in range(sz):
                    key = kw['name_list'][i]
                    val = kw['value_list'][i]
                    self.__dict__[key]=val
                for i in range(nm_size - sz):
                    key = kw['name_list'][sz+i]
                    val=''
                    self.__dict__[key]=val
                #self.value_list += kw['value_list'][:sz]
                #self.value_list += [''] * (nm_size - sz)
                kw.pop('value_list')
            #no value_list
            else:
                #self.value_list += [''] * nm_size
                for i in range(nm_size):
                    key = kw['name_list'][i]
                    val=''
                    self.__dict__[key]=val
            kw.pop('name_list')
        for key in kw:
            #print key
            #self.name_list.append(key)
            #self.value_list.append(kw[key])
            self.__dict__[key] = kw[key]
