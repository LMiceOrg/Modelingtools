#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Excel ModelDeclaration模型声明解析器
ExcelModelDeclarationParser

元模型定义表单

1: 实体程序模型：
    序号， 模型类别（大类，模型分类， 模型细类）， 中文名称， 英文名称，模型名称，
    模型编号， LVC分类，组件类型，功能要求，模型粒度，模型设计(功能，接口，算法），
    模型开发（框架，算法，代码)


"""
import excelsheetparser

class ExcelModelDeclarationParser(excelsheetparser.ExcelSheetParser):
    def ParseExcelSheet(self, model, xl_name, sh_ctx, sh_idx, sh_name):
        """ 解析 元模型定义 表单 """
        xl_name, sh_name = self.strip(xl_name, sh_name)
        #namespace is Global
        self.ns = self.default_ns

        md_no = ''
        md_type1 = ''
        md_type2 = ''
        md_type3 = ''
        md_cname = ''
        md_ename=''
        md_name=''
        md_serno=''
        md_lvc=''
        md_type =''
        md_req =''
        md_grain=''
        md_dfunc =''
        md_dintf=''
        md_dalgo=''
        md_cframe=''
        md_calgo=''
        md_ccode=''

        for i in range(1, len(sh_ctx)):
            if len(sh_ctx[i]) < 18:
                continue
            md_no, d_type1, md_type2, md_type3, md_cname, md_ename, md_name, md_serno, md_lvc, md_type, md_req, md_grain, md_dfunc, md_dintf, md_dalgo, md_cframe, md_calgo, md_ccode=self.strip(sh_ctx[i][:18])

            model.AppendItem(xl_name, sh_idx, sh_name, self.ns, "ModelDeclaration", (md_no, md_type1, md_type2, md_type3, md_cname, md_ename, md_name, [md_serno, md_lvc, md_type, md_req, md_grain, md_dfunc, md_dintf, md_dalgo, md_cframe, md_calgo, md_ccode]))
        #print "items:", item_cnt
