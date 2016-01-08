#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel ModelProperty表单解析器基类, 
ExcelModelPropertyParser

Sheet struct:
"""
import excelsheetparser

class ExcelModelPropertyParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)
        #model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "ModelProperty", (last_ed_type, last_ed_desc, last_ed_items))
    
