#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CPPheaderBuilder
CPP头文件建造者
"""

import basebuilder
import autotools
import baseitem

import time
import os
import re
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom
import web.template

render = web.template.render(os.path.split(os.path.realpath(__file__))[0],
globals={'type':type,"hasattr":hasattr})

#Array<Char,32>
adt_parser = re.compile("\s*(\w+)\s*[<]\s*(\w+)\s*[,]\s*([0-9]+)\s*[>]")

ad_header_name ="%s_Typedef" % autotools.l_ns_name


enumlist_template=u"""
namespace {ed_ns}
{{
/**
*@brief {ed_ns}::{ed_name} {ed_desc}
* 枚举类型定义
* 构建自 {src_path}
*
*/
enum {ed_name} {{
    {ed_items}
}};
}} /* end of namespace {ed_ns} */

/**LMice::is_pod 模板特化 */
namespace LMice{{
//is_pod
template<> struct is_pod<{ed_ns}::{ed_name}>:public LMice::cv<int,1>{{}};
}}//namespace LMice

"""

enumitem_template=u"""
    //{it_desc}
    {it_name} = {it_value}"""

enum_template=u"""
{ENUM}={value}"""

arraylist_template=u"""
/**
*@brief {ad_ns}::{ad_name} {ad_desc}
* 枚举类型定义
* 构建自 {src_path}
*
*/

typedef {it_ns}::Array<{it_ns}::{it_type},{it_num}> {ad_name};
"""

struct_template=u"""
namespace {cd_ns}
{{
/**
*@brief {cd_ns}::{cd_name} {cd_desc}
* 枚举类型定义
* 构建自 {part_name}
* 元模型自 {src_path}
*
*/
struct {cd_name}:public LMice::LMBaseClass< {cd_name} > {{
    {cd_items}

    /* Auto generated functions */
{cd_funcs}
}};
}} /* end of namespace {cd_ns} */
"""


structitem_template=u"""
    /**
    *@brief {it_type}::{it_name} {it_desc}
    *@name {it_cname} {it_grain}
    *@value {it_unit}: {it_default}, ({it_min}, {it_max})
    */
    {it_ns}::{it_type} {it_name};
"""

structdummy_template=u"""
    /**
    *@brief {it_type}::{it_name} {it_desc}
    *@name {it_cname} {it_grain}
    *@value {it_unit}: {it_default}, ({it_min}, {it_max})
    */
    LMBaseClass< {it_ns}::{it_type} > {it_name};
"""


msg_struct_template=u"""
namespace {cd_ns} {{
/**
*@brief {cd_ns}::{cd_type} {cd_desc}
* 枚举类型定义
* 构建自 {part_name}
* 元模型自 {src_path}
*
*/
struct {cd_type}:public LMice::LMBaseClass< {cd_type} > {{
    {cd_items}

    /* Auto generated functions */
{cd_funcs}
}};

}}
"""

class CPPHeaderBuilder(basebuilder.BaseBuilder):
    def __init__(self, datamodel, folder):
        super(CPPHeaderBuilder, self).__init__(datamodel)
        if type(folder) == str:
            self.folder = os.path.abspath(folder.decode('utf-8'))
        elif type(folder) == unicode:
            self.folder = folder
        else:
            raise TypeError("folder type (%s) is invalid!", str(type(folder)))
        self.props={}   
        self.outfiles = []
        


    def IsPod(self, type):
        if type in (u"String", u'Wstring') or type[:8] == 'LMVector':
            return False
        return True

    def CheckGrainItem(self, item):
        """ 规则: 复合数据结构中的多粒度参数解析 在列（粒度）的值为(1+), 其粒度数量是上一个字段
            其类型为string
        """
        if item.strip() == "1+":
            #variant-length sub-struct
            return True

        return False

    def CreateModelEventCPPHeader(self, item):
        """ 生成模型Event头文件"""
        is_pod = 1
        it_list = []

        pps = baseitem.BaseItem(['cd_name', 'cd_ns', 'cd_cname', 'cd_io', 'cd_desc', 'cd_var', 'cps'], item.item_val)
        pps.cd_type = pps.cd_name + "_T"

        pps.append(src_path=item.source, part_name=item.part_name)
        pps.append(is_pod=True, size='0', pack='', unpack='', clear='')

        pj_num, pj_name, pj_cname = self.SourceToProject(item)
        so_folder = '%s_%s' % (pj_num, pj_name)
        if not self.modelevts.has_key( so_folder ):
            self.modelevts[so_folder] = []

        self.modelevts[ so_folder ].append(pps)

        for cp in pps.cps:
            it = baseitem.BaseItem(['it_name', 'it_ns', 'it_cname', 'it_type', 'it_grain', 'it_unit',
                'it_default', 'it_min', 'it_max', 'it_desc', 'it_asign'], cp)

            if it.it_name == "":
                return

            #refinement namespace
            it.it_type, it.it_ns = self.RefineNamespace(it.it_type, it.it_ns)

            dp_val = "%s::%s" % (it.it_ns, it.it_type)
            if self.CheckGrainItem(it.it_grain):
                it.or_ns = it.it_ns
                it.or_type = it.it_type
                it.is_array = True
                it.it_grain="LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_type = "LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_ns = "LMice"#autotools.g_ns_name #Global namespace name
            if not self.IsPod(it.it_type):
                is_pod = 0
            it_list.append(structitem_template.format( **it.dict() ) )

            self.GenerateStructFunction(it, pps)

        pps.cd_items = u"\n".join(it_list)
        pps.cd_funcs = render.cd_funcs_tmpl(pps)

        ctx = msg_struct_template.format(**pps.dict() )

        dp_key = "%s::%s" % (pps.cd_ns, pps.cd_type)

        ctx += 'namespace LMice {\ntemplate<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n}//namespace LMice\n' % (dp_key, is_pod)


        self.props["msg_struct"] += ctx
        self.props['msg_pod'] += 'namespace LMice {\ntemplate<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n}//namespace LMice\n' % (dp_key, is_pod)


    def CreateModelMessageCPPHeader(self, item):
        """ 生成模型信息头文件"""
        is_pod = 1
        it_list = []

        pps = baseitem.BaseItem(['cd_name', 'cd_ns', 'cd_cname', 'cd_io', 'cd_desc', 'cd_var', 'cps'], item.item_val)
        pps.cd_type = pps.cd_name + "_T"

        pps.append(src_path=item.source, part_name=item.part_name)
        pps.append(is_pod=True, size='0', pack='', unpack='', clear='')

        pj_num, pj_name, pj_cname = self.SourceToProject(item)
        so_folder = '%s_%s' % (pj_num, pj_name)
        if not self.modelinfo.has_key( so_folder ):
            self.modelinfo[so_folder] = []

        self.modelinfo[ so_folder ].append(pps)

        for cp in pps.cps:
            it = baseitem.BaseItem(['it_name', 'it_ns', 'it_cname', 'it_type', 'it_grain', 'it_unit',
                'it_default', 'it_min', 'it_max', 'it_desc', 'it_asign'], cp)

            if it.it_name == "":
                return

            #refinement namespace
            it.it_type, it.it_ns = self.RefineNamespace(it.it_type, it.it_ns)

            dp_val = "%s::%s" % (it.it_ns, it.it_type)
            if self.CheckGrainItem(it.it_grain):
                it.or_ns = it.it_ns
                it.or_type = it.it_type
                it.is_array = True
                it.it_grain="LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_type = "LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_ns = "LMice"#autotools.g_ns_name #Global namespace name
            if not self.IsPod(it.it_type):
                is_pod = 0
            it_list.append(structitem_template.format( **it.dict() ) )

            self.GenerateStructFunction(it, pps)


        pps.cd_items = u"\n".join(it_list)
        pps.cd_funcs = render.cd_funcs_tmpl(pps)

        ctx = msg_struct_template.format(**pps.dict() )

        dp_key = "%s::%s" % (pps.cd_ns, pps.cd_type)

        ctx += 'namespace LMice {\ntemplate<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n}//namespace LMice\n' % (dp_key, is_pod)


        self.props["msg_struct"] += ctx
        self.props['msg_pod'] += 'template<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n' % (dp_key, is_pod)


    def CreateEnumCPPHeader(self, item):
        """ 生成枚举类型头文件的prop """
        ctx = item.item_val
        ed_type, ed_desc, ed_items = ctx[:3]
        listprop={"ed_ns":item.item_ns, "src_path":item.source}
        listprop["ed_name"] =ed_type
        listprop["ed_desc"] =ed_desc.replace('\n', ' ')
        listprop["ed_items"]= ''
        length=len(ed_items)
        i=1
        it_list = []
        for item in ed_items:

            i=i+1
            enumprop={}
            it_name, it_value, it_desc = item[:3]
            it_desc = it_desc.replace('\n', ' ')
            it_value=int(it_value)

            it_list.append( enumitem_template.format(it_name=it_name, it_value=it_value, it_desc=it_desc) )

        listprop["ed_items"] = u',\n'.join(it_list)
        ctx = enumlist_template.format(** listprop)  
        self.props["enumlist"] = self.props["enumlist"]+ctx
        
    def CreateArrayCPPHeader(self, item):
        """ 生成数组类型头文件的prop name<num>"""
        ctx = item.item_val
        ad = baseitem.BaseItem(['ad_name', 'it_ns', 'it_type', 'it_num', 'it_unit', 'ad_desc'], ctx[:6])
        ad.append(['ad_ns', 'src_path'],[item.item_ns, item.source])
        ad.it_type, ad.it_ns = self.RefineNamespace(ad.it_type, ad.it_ns)

        #ad_name, ad_desc, ad_type, ad_dim = ctx[:4]
        #listprop={"ad_ns":item.item_ns, "src_path":item.source}
        #listprop['ad_desc'] = ad_desc
        #listprop["ad_name"] = ad_name
        #ad_val = adt_parser.findall(ad.ad_type)
        #if len(ad_val) == 1:
        #ad.append(['ad_name', 'it_ns', 'it_name', 'it_num', 'it_unit', 'ad_desc'], ad_val[0])
        #it_type, it_name, it_num = ad_val[0]

        #listprop["ad_type"] =it_name.lower()
        #listprop["ad_num"] = it_num
        #ad.append(it_num=it_num, it_type=it_name, it_ns=it_ns)
        #print ad
        ctx = arraylist_template.format(** ad.dict())
        self.props["arraylist"] = self.props["arraylist"]+ctx

    def GenerateStructFunction(self, it, cd):
        is_pod = self.IsPod(it.it_type)
        default_value = None
        for k in autotools.dt_mapping:
            if autotools.dt_mapping[k][0] == it.it_type:
                default_value = autotools.dt_mapping[k][2]
        if default_value != None:
            default_value = "%s%s = %s;\n" % (' '*8, it.it_name, default_value)
        else:
            if it.it_type[:5] == 'Enum_':
                default_value = "%s%s = %s_0;\n" % (' '*8, it.it_name, it.it_type)
            elif it.it_type[:10] == 'Wstring255':
                default_value = "%smemset(&%s, 0, sizeof(%s));\n" % (' '*8, it.it_name, it.it_name)
            else:
                default_value = "%s%s.clear();\n" % (' '*8, it.it_name)
        if not is_pod:
            cd.is_pod = is_pod
            cd.size += " + %s.size()" % it.it_name
            cd.pack +=      "            %s.pack(buffer+pos, buffer_size-pos);\n            pos += %s.size();\n" % ((it.it_name,)*2)
            cd.unpack +=    "            %s.unpack(buffer+pos, buffer_size-pos);\n            pos += %s.size();\n" % ((it.it_name,)*2)
            cd.clear += default_value#    "        %s.clear();\n" % it.it_name
        else:
            cd.size += " + sizeof(%s)" % it.it_name
            cd.pack +=  "            memcpy(buffer+pos, &%s, sizeof(%s));\n            pos += sizeof(%s);\n" % ((it.it_name,)*3)
            cd.unpack +="            memcpy(&%s, buffer+pos, sizeof(%s));\n            pos += sizeof(%s);\n" % ((it.it_name,)*3)
            cd.clear += default_value#"        memset(&%s, 0, sizeof(%s));\n" % ((it.it_name,)*2)
        it.is_pod = is_pod
    def CreateCompCPPHeader(self,item):
        """ 生成复合结构体类型头文件的prop """
        ctx = item.item_val
        cd_name, cd_desc, cd_items = ctx[:3]
        cd_ns = item.item_ns
        listprop={"cd_ns":item.item_ns, "src_path":item.source, "part_name":item.part_name}
        listprop['cd_desc'] = cd_desc
        listprop["cd_name"] = cd_name
        it_list =[]
        it_plist=[]
        #Set default pod value
        is_pod = True

        cd = baseitem.BaseItem(['its', 'is_pod', 'size'], [[], True, '0'])
        cd.append(pack='', unpack='', clear='')

        dp_key = "%s::%s" % (cd_ns, cd_name)
        has_depends = False
        for  item in cd_items:
            it = baseitem.BaseItem(['it_name', 'it_ns', 'it_cname', 'it_type', 'it_grain', 'it_unit', 'it_default', 'it_min', 'it_max', 'it_desc'], item[:10])
            #it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item[:10]
            #refinement namespace
            it.it_type, it.it_ns = self.RefineNamespace(it.it_type, it.it_ns)

            dp_val = "%s::%s" % (it.it_ns, it.it_type)
            pre_decl = "namespace %s { struct %s; }\n" % (it.it_ns, it.it_type)
            otp, ons = it.it_type, it.it_ns
            if self.CheckGrainItem(it.it_grain):
                it.or_ns = it.it_ns
                it.or_type = it.it_type
                it.is_array = True
                it.it_grain="LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_type = "LMVector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_ns = "LMice"#autotools.g_ns_name #Global namespace name


            if ons.strip() != autotools.g_ns_name: #Global namespace name
                if otp[:5] == "Enum_":
                    pass
                elif autotools.dt_mapping.values().count( (otp, ons)) == 0:
                    self.props["predeclare"].add(pre_decl)


                    if self.depends.has_key(dp_key):
                        if self.depends[dp_key].count(dp_val) > 0:
                            pass
                        else:
                            self.depends[dp_key].append(dp_val)
                    else:
                        self.depends[dp_key] = [ dp_val ]

                    has_depends = True
            self.GenerateStructFunction(it, cd)

            is_pod = cd.is_pod

            #it_list.append( structitem_template.format(it_name=it_name, it_ns=it_ns, it_cname=it_cname, it_type=it_type, it_grain=it_grain, it_unit=it_unit, it_default=it_default, it_min=it_min, it_max=it_max, it_desc=it_desc) )
            #print it
            #cd.its.append(it)

            it_list.append(structitem_template.format( **it.dict() ) )

        self.dep_pod[dp_key] =[dp_key, is_pod]
        listprop["cd_items"] = u"\n".join(it_list)
        #print cd
        listprop["cd_funcs"] = render.cd_funcs_tmpl(cd)
        ctx = struct_template.format(**listprop)  + 'namespace LMice {\ntemplate<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n} //namespace LMice\n' % (dp_key, int(is_pod) )
        if has_depends:
            self.depvalue[dp_key] =ctx
            #print "%s --> %s" % (dp_key, str(self.depends[dp_key]) )
        else:
            self.props["structlist"] = self.props["structlist"] + ctx
            self.props['is_pod'] += 'template<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n' % (dp_key, int(is_pod) )
            #print dp_key
        


    def writeCPPHeaderFile(self):
        """ Write C++ header files """

        # CompData hpp
        ctx = render.cd_hpp_tmpl(self.props)
        name = os.path.join(self.props["pj_path"], "%s.h" % self.props["h_name"])
        self.SaveFile(ctx, name)

        # EnumData hpp
        ctx = render.ed_hpp_tmpl(self.props)
        name = os.path.join(self.props["pj_path"], "%s_Enum.h" % self.props["h_name"])
        self.SaveFile(ctx, name)
     
    def WriteArrayHeaderFile(self):
        """ 枚举类型 数组类型与别名 """
        #print autotools.gen_g_ns_type
        self.props['autotools'] = autotools
        self.props["globaltypedefs"]=autotools.gen_g_ns_type()

        self.props['enumlist']= ''
        for ns in self.GetNamespaces():
            self.props['enumlist'] += '#include "%s_Enum.h"\n' % ns.lower()
        self.props['enumlist'] = self.GetNamespaces()
        self.props["H_NAME"] = ad_header_name.upper()

        # ArrayData hpp
        name = os.path.join(self.props["pj_path"], "%s.h" % ad_header_name)
        ctx =render.ad_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)

        # DataDefile hpp
        name = os.path.join(self.props["pj_path"], "DataDefine.h" )
        ctx = render.dd_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)

        # Param Check hpp
        name = os.path.join(self.props["pj_path"], "ParameterCheck.h" )
        ctx = render.pc_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)

    def CreateModelPerformanceHeader(self, item):
        md_name, ns, md_cname, md_desc, md_items = item.item_val
        defs = []
        for i in range( len(md_desc)):
            it = baseitem.BaseItem(['it_name', 'it_ns', 'it_cname', 'it_type', 'it_grain', 'it_unit', 'it_default', 'it_min', 'it_max', 'it_desc'], md_desc[i] )
            it.it_type, it.it_ns = self.RefineNamespace(it.it_type, it.it_ns)
            otp, ons = it.it_type, it.it_ns
            if self.CheckGrainItem(it.it_grain):
                it.or_ns = it.it_ns
                it.or_type = it.it_type
                it.is_array = True
                it.it_grain="vector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_type = "vector<%s::%s>" % (it.it_ns, it.it_type)
                it.it_ns = "std"#autotools.g_ns_name #Global namespace name
            defs.append(it)
        self.modelperf[md_name] = defs


    def CreateDependsHeaderFile(self):
        if len(self.depends) ==0:
            return
        for key in self.depends:
            has_depend = False
            _k = key
            _vs = self.depends[key]
            _pod = self.dep_pod[key]
            pod_list = [ _pod[1] ]
            for _v in _vs:
                if self.depends.has_key(_v):
                    has_depend = True
                    pod_list.append(self.dep_pod[key][1])
                    break
            if not has_depend:
                #print _k, pod_list.count(False)
                self.dep_pod[_k][1] = pod_list.count(True) == len(pod_list)
                self.props['is_pod'] += 'template<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n' % (_k, int(self.dep_pod[_k][1]) )
                self.deplist = self.deplist + self.depvalue[_k]
                self.depends.pop(_k)
                break
        self.CreateDependsHeaderFile()
        #a-->[b ,d]
        #b-->c

    def WriteLocalHeaderFile(self):
        """ 模型开发入口 头文件 """

        self.props["h_name"] =autotools.l_ns_name.lower()
        self.props["H_NAME"] = autotools.l_ns_name.upper()
        self.props['deplist'] = self.deplist
        self.props['headers'] = self.GetNamespaces()

        name = os.path.join(self.props["pj_path"], "%s.h" % autotools.l_ns_name)
        ctx = render.pj_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)

        self.props["h_name"] =autotools.l_ns_name.lower()+ "_Depends"
        self.props["H_NAME"] =self.props["h_name"].upper()
        name = os.path.join(self.props["pj_path"], "%s_Depends.h" % autotools.l_ns_name)
        ctx = render.dp_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)

    def WriteModelHeaderFile(self):
        """ 模型 消息与事件头文件 """
        self.props["h_name"] =autotools.l_ns_name.lower()+ "_Model"
        self.props["H_NAME"] =self.props["h_name"].upper()

        name = os.path.join(self.props["pj_path"], "%s_Model.h" % autotools.l_ns_name)
        ctx = render.md_hpp_tmpl(self.props)
        self.SaveFile(ctx, name)


    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        self.elements = {}
        self.outfiles = []
        self.modelperf = {} #存储模型性能参数列表
        self.modelevts = {} #存储模型事件列表
        self.modelinfo = {} #存储模型信息列表
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个CPP头文件 """

        #print self.GetNamespaces()
        self.depends={} #struct --> {struct}
        self.depvalue={}
        self.deplist=""
        self.dep_pod = {} #id --> 1/0

        self.props = {}
        self.props['local_ns_name'] = autotools.l_ns_name
        self.props['l_typedef'] = ad_header_name
        self.props["user_name"] = "LMiced Org"
        self.props['user_dept'] = 'Tsinghua'
        self.props["tm_now"] =time.strftime("%Y-%m-%d %H:%M:%S")
        self.props["pj_path"] =self.folder
        self.props["arraylist"]=''
        #model message and event
        self.props["msg_struct"] = ''
        self.props["msg_pod"] = ''

        #创建Namespace element
        for ns in self.GetNamespaces():#namespace表示各种不同的类，平台类、传感器器类，

            #print ns, len(self.GetItemByNamespace(ns))
            last_ad_str  = self.props["arraylist"]
            self.props["arraylist"]=''
            self.props['is_pod']=''

            self.props["h_name"] =ns
            self.props["H_NAME"] = ns.upper()
            self.props["enumlist"]=''

            self.props["structlist"]=''
            self.props["predeclare"] = set()
            for item in self.GetItemByNamespace(ns):
                #print item.item_type
                if item.item_type == "EnumData":    #枚举类型
                    #print "enum item"
                    self.CreateEnumCPPHeader(item)#在头文件中加入值
                elif item.item_type == "ArrayData":   #数组类型
                    #print "array"
                    self.CreateArrayCPPHeader(item)
                elif item.item_type == "CompData":    #复合结构
                    #print "Comp data"
                    self.CreateCompCPPHeader(item)
                elif item.item_type == "ModelMessage":    #模型消息
                    self.CreateModelMessageCPPHeader(item)
                elif item.item_type == "ModelEvent":    #模型事件
                    self.CreateModelEventCPPHeader(item)
                elif item.item_type == "ModelPerformance": #模型性能参数
                    self.CreateModelPerformanceHeader(item)

            self.props["predeclare"] = "\n".join(self.props["predeclare"])
            if len(self.props["arraylist"]) > 0:
                self.props["arraylist"] = "%snamespace %s {\n\n%s\n\n} /* namespace %s */\n" % (last_ad_str, ns, self.props["arraylist"], ns)
            else:
                self.props["arraylist"] = last_ad_str
            self.writeCPPHeaderFile()
        self.WriteArrayHeaderFile()
        #Clean is_pod
        self.props['is_pod'] = ''
        self.CreateDependsHeaderFile()
        self.WriteModelHeaderFile()

        self.WriteLocalHeaderFile()


    def BuildEnd(self):
        """结束构建 关闭所有头文件 """
        '''for ns in self.elements:
            root = self.elements[ns]
            self.SaveNamespaceFile(ns, root)'''

    def GetFiles(self):
        outfiles = []
        for f in self.outfiles:
            outfiles.append( f.encode('utf-8') )
        return outfiles
