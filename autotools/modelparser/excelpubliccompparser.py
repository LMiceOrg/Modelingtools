#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel PublicComp表单解析器基类, 由公共数据类型定义文件生成复合结构类型
ExcelPublicCompParser

Sheet struct: (复合结构数据类型名称 ns 数据类型描述 数据项名称 ns1
        数据项中文名称 数据项数据类型 粒度 单位 默认值 最小值 最大值 数据项描述)
        
"""
import excelsheetparser

class ExcelPublicCompParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)
        #print "CompData", self.ns
        last_cp_name=""
        last_cp_ns = ""
        last_cp_desc =""
        last_cp = []
        
        #枚举行
        for i in range(1, len(sh_ctx)):
            if len(sh_ctx[i]) <12:
                raise ValueError(u"[%s]:[%s] CompData sheet cols error, should be 12, but(%d)" % ( xl_name, sh_name, len(sh_ctx[i]) ) )
            cp_name, cp_desc, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = sh_ctx[i][:12]
            cp_ns = self.ns

            cp_name = cp_name.strip()
            it_name = it_name.strip()
            it_ns   = it_ns.strip()
            it_type = it_type.strip()
            cp_ns, cp_name = self.VerifyNsName(cp_ns, cp_name)
            #print "Original:", it_ns, it_type
            it_ns, it_type= self.VerifyNsName(it_ns, it_type)

            #print "Result:",it_ns, it_type
            # if got new compdata name
            if cp_name != "":
                # if has already got compdata ctx
                if last_cp_name != "" and len(last_cp) > 1:
                    model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "CompData", (last_cp_name, last_cp_desc, last_cp))
                # new compdata
                last_cp_name = cp_name
                last_cp_ns = cp_ns
                last_cp_desc = cp_desc
                last_cp = []
            # append item data
            if it_name == "":
                continue
            last_cp.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc] )
        # process the last compdata
        if last_cp_name != "" and len(last_cp) >0:
            model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "CompData", (last_cp_name, last_cp_desc, last_cp))
        
