#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Excel 格式 模型性能参数解析器
　 ExcelModelPerfParser

  Excel:实体模型名称	中文名称	变量名称	变量命名空间
  变量中文名称	变量数据类型	粒度
  单位	默认值	最小值
  最大值	描述	数值

  Start Row := 2
"""

import excelsheetparser

class ExcelModelPerfParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)
        #print sh_name.encode('utf-8'), 'ExcelModelPerfParser'
        #the perf need look for each cols
        last_md_name=""
        last_md_cname =""

        if len(sh_ctx) <3:
            return
        #print len(sh_ctx)
        #print str(sh_ctx[2]), len(sh_ctx[2])
        if len(sh_ctx[2]) <13:
            return
        cols = len(sh_ctx[2]) - 12
        md_items=[[]]*cols
        md_desc = []

        for row in range(2, len(sh_ctx)):
            it_val =''
            md_name, md_cname, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc=sh_ctx[row][:12]
            #print cols, len(sh_ctx[row])
            for col in range(cols):
                #print col
                it_val = sh_ctx[row][12+col]
                md_items[col].append(it_val)
            md_desc.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc])
            if md_name != "":
                last_md_name = md_name
                last_md_cname = md_cname

        #store
        model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "ModelPerformance", (last_md_name, self.ns, last_md_cname, md_desc, md_items))

