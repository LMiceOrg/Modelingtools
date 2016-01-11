#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datamodelgenerator
import os
import cPickle as pickle
#import pickle

gen = datamodelgenerator.XLDataModelGenerator()

def Init():
    gen = datamodelgenerator.XLDataModelGenerator()

def GetFileList(*args, **kw):
    return gen.GetFileList(*args, **kw)

def CheckExcelFileModel(*args, **kw):
    return gen.CheckExcelFileModel(*args, **kw)

def ParseSources(*args, **kw):
    #print "GenerateDataStruct"
    return gen.Parse(*args, **kw)

def SaveDataStruct(*args, **kw):
    return gen.BuildDataStruct(".")

def SaveModelDesc(*args, **kw):
    return gen.BuildModelDesc('.')

def SaveCppProject(*args, **kw):
    return gen.BuildMsvc2008Solution('.')

def CheckFistParamAsFile(fn,*args, **kw):
    def wrapped(*args, **kw):
        if kw.has_key('file'):
            name = kw['file']
        elif len(args) >= 1:
            name = args[0]
        else:
            raise AttributeError("file name parameter not given")

        if type(name) == str:
            name = name.decode('gbk')
        elif not type(name) == unicode:
            raise TypeError("file name type must be string")

        kw['file']=name
        return fn(*args, **kw)

    return wrapped

@CheckFistParamAsFile
def Restore(*args, **kw):
    name = kw['file']
    f=open(name, "rb")
    global gen
    gen = pickle.load(f)
    f.close()

@CheckFistParamAsFile
def Backup(*args, **kw):
    name = kw['file']
    f=open(name, "wb")
    pickle.dump(gen, f)
    f.close()

def GetSourceList(*args, **kw):
    slist = gen.GetSources()
    utf8list = []
    for s in slist:
        if type(s) == unicode:
            utf8list.append( s.encode('utf-8') )
        elif type(s) == str:
            utf8list.append(s)
    return utf8list

def GetModelProjectName(*args, **kw):
    return gen.GetProjectRoot()
