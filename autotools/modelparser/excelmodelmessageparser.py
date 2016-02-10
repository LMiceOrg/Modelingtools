#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel ModelMessage表单解析器基类, 
ExcelModelMessageParser

Sheet struct: 信息名称 中文名称 输入输出类型 接口描述 是否可变长 变量名称 变量中文名称
变量数据类型 粒度 单位 默认值 最小值 最大值 属性描述 赋值方法

        
"""
import excelsheetparser

class ExcelModelMessageParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):

        #get namespace
        self.GetNamespace(xl_name, sh_idx, sh_name)

        last_cp_cname=""
        last_cp_name=""
        last_cp_ns = ""
        last_cp_desc =""
        last_cp_io=""
        last_cp_var=""
        last_cp = []
        
        for i in range(2, len(sh_ctx)):
            if len(sh_ctx[i]) == 15:
                #print len(sh_ctx), len(sh_ctx[i])
                raise TypeError("ExcelFile(%s) Sheet[%s] is old style(15 cols)!" %(xl_name.encode('utf-8'), sh_name.encode('utf-8')))
            if len(sh_ctx[i]) <17:
                continue
            #cp_io :输入输出类型  cp_var:是否可变长
            cp_name, cp_ns, cp_cname, cp_io, cp_desc, cp_var, it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc, it_asign = sh_ctx[i][:17]
            if cp_ns == "":
                cp_ns = self.ns

            cp_ns = cp_ns.strip()
            cp_name = cp_name.strip()
            it_name = it_name.strip()
            it_ns   = it_ns.strip()
            it_type = it_type.strip()
            cp_ns, cp_name = self.VerifyNsName(cp_ns, cp_name)
            #print "Original:", it_ns, it_type
            it_ns, it_type= self.VerifyNsName(it_ns, it_type)
            # if got new compdata name
            if cp_name != "":
                # if has already got compdata ctx
                if last_cp_name != "" and len(last_cp) > 0:
                    model.AppendItem(xl_name, sh_idx, sh_name, last_cp_ns, "ModelMessage",(
                        last_cp_name, last_cp_ns, last_cp_cname, last_cp_io, last_cp_desc, last_cp_var, last_cp))
                # new compdata
                last_cp_name = cp_name
                last_cp_ns = cp_ns
                last_cp_cname = cp_cname
                last_cp_io = cp_io
                last_cp_desc = cp_desc
                last_cp_var = cp_var
                last_cp = []
            # append item data
            last_cp.append([it_name, it_ns, it_cname, it_type, it_grain, it_unit,
                            it_default, it_min, it_max, it_desc, it_asign] )
        # process the last compdata
        if last_cp_name != "" and len(last_cp) >0:
            model.AppendItem(xl_name, sh_idx, sh_name, last_cp_ns, "ModelMessage",(
                last_cp_name, last_cp_ns, last_cp_cname, last_cp_io, last_cp_desc, last_cp_var, last_cp))
        
