#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel PublicEnum表单解析器基类, 
ExcelPublicEnumParser

Sheet struct: 枚举数据类型名称	数据类型描述	枚举项	值	值定义
        
"""
import excelsheetparser

class ExcelPublicEnumParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)
        #print "Namespace",self.ns, sh_name, len(sh_ctx)
        #item_cnt = 0
        last_ed_type = ''
        last_ed_desc = ''
        last_ed_items = []
        for i in range(1, len(sh_ctx)):
            if len(sh_ctx[i])<5:
                continue
            ed_type, ed_desc, it_name, it_value, it_desc = sh_ctx[i][:5]
            if ed_type != "":
                if last_ed_type != "":
                    #item_cnt = item_cnt +1
                    model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "EnumData", (last_ed_type, last_ed_desc, last_ed_items))
                #new enumdata
                last_ed_type = ed_type
                last_ed_desc = ed_desc
                last_ed_items = []
            #append item data
            last_ed_items.append((it_name, it_value, it_desc))
        #process the last one
        if len(last_ed_items) >0:
            model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "EnumData", (last_ed_type, last_ed_desc, last_ed_items))
        #print "items:", item_cnt
