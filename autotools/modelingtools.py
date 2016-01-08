#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datamodelgenerator
asdas
gen = datamodelgenerator.XLDataModelGenerator()

def Init():
    gen = datamodelgenerator.XLDataModelGenerator()

def GetFileList(*args, **kw):
    return gen.GetFileList(*args, **kw)

def CheckExcelFileModel(*args, **kw):
    return gen.CheckExcelFileModel(*args, **kw)

def GenerateDataStruct(*args, **kw):
    #print "GenerateDataStruct"
    return gen.Parse(*args, **kw)

def SaveDataStruct(*args, **kw):
    return gen.BuildDataStruct(".")

def SaveModelDesc(*args, **kw):
    return gen.BuildModelDesc('.')
