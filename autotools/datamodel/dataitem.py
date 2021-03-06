#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DataItem
数据项基类


"""

class DataItem(object):
    def __init__(self, *args):
        self.Names=['source',
           'part_idx',
           'part_name',
           'item_ns',
           'item_type',
           'item_val']
        self.Values=[]
        cnt = 0
        for arg in args:
            if type(arg) == str:
                arg = arg.decode('gbk').strip()
            elif type(arg) == unicode:
                arg = arg.strip()
            self.Values.append(arg)
            cnt = cnt + 1
            if cnt == len(self.Names):
                break
        for i in range(len(self.Values), len(self.Names) ):
            self.Values.append(None)
    #list method
    def __getitem__(self, idx):
        return self.Values[idx]
    def __len__(self):
        return len(self.Values)
    #dict method
    def __getattr__(self, name):
        if name in ('source','part_idx','part_name','item_ns','item_type','item_val') > 0:
            return self.Values[self.Names.index(name)]
        else:
            # Default behaviour
            return object.__getattribute__(self, name)
    #def __setattr__(self, name, val):
    #self.Values[self.Names.index(name)] = val
