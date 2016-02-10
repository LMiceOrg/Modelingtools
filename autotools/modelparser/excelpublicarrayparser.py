#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel PublicArray表单解析器基类, 由公共数据类型定义文件生成数组类型
ExcelPublicEnumParser

Sheet struct: 数组数据类型名称 数据项命名空间 数据项数据类型 数组维数 数据项单位 数据类型描述


"""
import excelsheetparser

class ExcelPublicArrayParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)
        
        for i in range(1, len(sh_ctx)):
            if len(sh_ctx[i]) < 6:
                continue
            ad_name, it_ns, it_type, it_num, it_unit, ad_desc = sh_ctx[i][:6]
            #ignore empty row
            if ad_name == "":
                continue
            #print "array:",self.ns,ad_name
            it_num = str(int(it_num))
            model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "ArrayData", (ad_name, it_ns, it_type, it_num, it_unit, ad_desc))
            #print len(model.GetItemByNamespace(self.ns)),model.GetItemByNamespace(self.ns)[-1].item_type,model.GetItemByNamespace(self.ns)[-1][5]
    
