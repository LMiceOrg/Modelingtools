#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel ModelInitParam表单解析器基类, 
ExcelModelInitParamParser

Sheet struct: 实体模型名称 中文名称 变量名称 变量中文名称 变量数据类型 数值 粒度 单位
默认值	最小值	最大值 描述
"""
import excelsheetparser

class ExcelModelInitParamParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)

        last_mp_name = ""
        last_mp_cname = ""
        mp_items=[]
        #Loop each row from 2
        for i in range(2, len(sh_ctx) ):
            it_ns = ""
            if len(sh_ctx[i]) < 11:
                continue
            if len(sh_ctx[i]) == 11:
                mp_name, mp_cname, it_name, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = sh_ctx[i][:11]
            else:
                mp_name, mp_cname, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = sh_ctx[i][:12]
            if last_mp_name == "":
                last_mp_name = mp_name
                last_mp_cname = mp_cname
            mp_items.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc])
        model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "ModelInitParam", (last_mp_name, last_mp_cname, mp_items))
    
