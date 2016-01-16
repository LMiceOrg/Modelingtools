#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" CPPheaderBuilder
CPP头文件建造者
"""

import basebuilder

import time
import os
import re
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom

#Array<Char,32>
adt_parser = re.compile("\s*(\w+)\s*[<]\s*(\w+)\s*[,]\s*([0-9]+)\s*[>]")

ad_header_name ="%s_Typedef" % basebuilder.l_ns_name

version_template = u"""/****************************************************************************
**
**	开发单位：{user_dept}
**	开发者：{user_name}
**	创建时间：{tm_now}
**	版本号：V1.0
**	描述信息：{h_name}
****************************************************************************/
"""

ad_template=version_template + u"""
#ifndef {H_NAME}_TYPEDEFS_H_
#define {H_NAME}_TYPEDEFS_H_

#include <string>
#include <cstdint>
#include <string.h>

/** 全局类型别名 */
{globaltypedefs}

/** 数组类型与别名 */
{arraylist}

/** 各命名空间的枚举类型定义 */
{enumlist}

namespace LMice {{

//enum value is_pod
template<class _Tp, _Tp __v> struct cv {{
    enum{{ value =       __v}};
    typedef _Tp         value_type;
    typedef cv          type;
}};

// Default pod is 0
template<class T> struct is_pod: public LMice::cv<int, 0> {{}};
template<> struct is_pod<int>: public LMice::cv<int, 1>{{}};

template <class TSubClass>
struct LMBaseClass
{{
    typedef LMBaseClass<TSubClass>  this_type;

    inline int size() const {{
        const TSubClass* p = static_cast<const TSubClass*>(this);
        return p->OnSize();
    }}

    int OnSize() const {{
        // 总是 返回 类型的大小
        //如果是可变长度类型，需要用户重载此函数
        return sizeof(TSubClass);
    }}

    inline void swap(this_type& x) const {{
        this_type c(x);
        x = *this;
        *this = c;
    }}

    inline char* data() const {{
        // 只提供 POD类型时的访问
        if(is_pod()) {{
            return reinterpret_cast<char*>(this);
        }} else {{
            return NULL;
        }}
    }}

    inline int pack(char* buffer, int buffer_size) const {{
        TSubClass* p = static_cast<TSubClass*>(this);
        return p->OnPack(buffer, buffer_size);
    }}

    int OnPack(char* buffer, int buffer_size) const {{
        int ret = -1;
        // 非POD类型，以及buffer太小情况的pack处理，由用户实现处理
        if(is_pod()) {{
            if(size() <= buffer_size) {{
                memcpy(buffer, (char*)this, size());
                ret = 0;
            }}
        }}
        return ret;
    }}

    inline int unpack(const char* buffer, int buffer_size) {{
        TSubClass* p = static_cast<TSubClass*>(this);
        return p->OnUnpack(buffer, buffer_size);
    }}

    int OnUnpack(const char* buffer, int buffer_size) {{
        int ret = -1;
        // 非POD类型，以及buffer_size太小情况的unpack处理，由用户实现处理
        if(is_pod()) {{
            if(size() <= buffer_size) {{
                memcpy((char*)this, buffer, size());
                ret = 0;
            }}
        }}
        return ret;
    }}


    inline bool is_pod() const {{
        return LMice::is_pod<TSubClass>::value;
    }}

    inline void clear() {{
        TSubClass* p = static_cast<TSubClass*>(this);
        p->OnClear();
    }}

    void OnClear() {{
        //在POD类型时，调用memset初始化
        //非POD类型，用户重载此函数
        if(is_pod()) {{
            memset(this, 0, size());
        }}
    }}



#if __cplusplus >= 199711L
    // c++0x 标准扩展
#endif

#if __cplusplus >= 201103L
    // c++11 标准扩展
protected:
    // 不允许直接实例化基类
    LMBaseClass() = default;
#endif

}};

}} /* end namespace LMice */

#endif // {H_NAME}_TYPEDEFS_H_

"""
eh_template=version_template + u"""
#ifndef {H_NAME}_ENUMDATA_H_
#define {H_NAME}_ENUMDATA_H_

namespace {h_name}
{{

/** 枚举类型 */
{enumlist}

}} /* end of namespace {h_name} */

#endif //{H_NAME}_ENUMDATA_H_

"""
h_template=version_template + u"""
#ifndef {H_NAME}_COMPDATA_H_
#define {H_NAME}_COMPDATA_H_

#include "{l_typedef}.h"

/** 引用类型声明 */
{predeclare}

namespace {h_name}
{{

/** 复合结构体类型 */
{structlist}

}} /* end of namespace {h_name} */

/** LMice::is_pod 模版特化 */
namespace LMice {{
{is_pod}
}}


#endif //{H_NAME}COMPDATA__H_

"""

enumlist_template=u"""
/**
*@brief {ed_ns}::{ed_name} {ed_desc}
* 枚举类型定义
* 构建自 {src_path}
*
*/
enum {ed_name} {{
    {ed_items}
}};

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
typedef {ad_type} {ad_name}[{ad_num}];"""

struct_template=u"""
/**
*@brief {cd_ns}::{cd_name} {cd_desc}
* 枚举类型定义
* 构建自 {part_name}
* 元模型自 {src_path}
*
*/
struct {cd_name}:public LMice::LMBaseClass< {cd_name} > {{
    {cd_items}
}};
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

#建模开发头文件
local_header_template=version_template + u"""
#ifndef LOCAL_{H_NAME}_H_
#define LOCAL_{H_NAME}_H_

#include "{local_ns_name}_Typedef.h"

#pragma pack(1)

{headers}

//有依赖顺序的结构体
#include "{local_ns_name}_Depends.h"


#pragma pack()

#endif //LOCAL_{H_NAME}_H_
"""

depends_template=version_template + u"""
#ifndef {H_NAME}_ENUMDATA_H_
#define {H_NAME}_ENUMDATA_H_

/** 顺序依赖结构体定义 */
{deplist}

/** LMice::is_pod 模版特化 */
namespace LMice {{
{is_pod}
}}

#endif //{H_NAME}_ENUMDATA_H_

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
        if type in (u"String", u'Wstring'):
            return False
        return True
    def CheckGrainItem(self, item):
        """ 规则: 复合数据结构中的多粒度参数解析 在列（粒度）的值为(1+), 其粒度数量是上一个字段
            其类型为string
        """
        if item[4].strip() == "1+":
            #variant-length sub-struct
            return True

        return False

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
        ad_name, ad_desc, ad_type, ad_dim = ctx[:4]
        listprop={"ad_ns":item.item_ns, "src_path":item.source}
        listprop['ad_desc'] = ad_desc
        listprop["ad_name"] = ad_name
        ad_val = adt_parser.findall(ad_type)
        if len(ad_val) == 1:
            it_type, it_name, it_num = ad_val[0]
            listprop["ad_type"] =it_name.lower()
            listprop["ad_num"] = it_num
            ctx = arraylist_template.format(** listprop)
            self.props["arraylist"] = self.props["arraylist"]+ctx

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

        dp_key = "%s::%s" % (cd_ns, cd_name)
        has_depends = False
        for  item in cd_items:
            it_name, it_ns, it_cname, it_type, it_grain, it_unit, it_default, it_min, it_max, it_desc = item[:10]
            #refinement namespace
            it_type, it_ns = self.RefineNamespace(it_type, it_ns)

            if self.CheckGrainItem(item):
                it_type = "String"
                it_ns = basebuilder.g_ns_name #Global namespace name
                it_grain="Array<%s::%s>" % (it_ns, it_type)
            if it_ns != basebuilder.g_ns_name: #Global namespace name
                if it_type[:5] == "Enum_":
                    pass
                elif basebuilder.dt_mapping.values().count( (it_type, it_ns)) == 0:
                    self.props["predeclare"].add("namespace %s { struct %s; }\n" % (it_ns, it_type) )

                    dp_val = "%s::%s" % (it_ns, it_type)
                    if self.depends.has_key(dp_key):
                        if self.depends[dp_key].count(dp_val) > 0:
                            pass
                        else:
                            self.depends[dp_key].append(dp_val)
                    else:
                        self.depends[dp_key] = [ dp_val ]

                    has_depends = True
            if not self.IsPod(it_type):
                is_pod = False

            it_list.append( structitem_template.format(it_name=it_name, it_ns=it_ns, it_cname=it_cname, it_type=it_type, it_grain=it_grain, it_unit=it_unit, it_default=it_default, it_min=it_min, it_max=it_max, it_desc=it_desc) )

        self.dep_pod[dp_key] =[dp_key, is_pod]
        listprop["cd_items"] = u"\n".join(it_list)
        ctx = struct_template.format(**listprop)
        if has_depends:
            self.depvalue[dp_key] ="namespace %s {\n%s\n}\n" % (cd_ns, ctx)
            #print "%s --> %s" % (dp_key, str(self.depends[dp_key]) )
        else:
            self.props["structlist"] = self.props["structlist"] + ctx
            self.props['is_pod'] += 'template<> struct is_pod<%s>:public LMice::cv<int, %d>{};\n' % (dp_key, int(is_pod) )
            #print dp_key
        
    def writeCPPHeaderFile(self):
        """ 写头文件 """
        ctx = h_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "common", "include", "%s.h" % self.props["h_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

        ctx = eh_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "common", "include", "%s_Enum.h" % self.props["h_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)
     
    def WriteArrayHeaderFile(self):
        """ 枚举类型 数组类型与别名 """
        #print basebuilder.gen_g_ns_type
        gns="namespace %s {\n\n" % basebuilder.g_ns_name
        tps = basebuilder.gen_g_ns_type()
        for key in tps:
            gns = gns + "typedef %s %s;\n" % (tps[key], key[0])
        gns = gns + "}\n"
        self.props["globaltypedefs"]=gns

        self.props['enumlist']= ''
        for ns in self.GetNamespaces():
            self.props['enumlist'] += '#include "%s_Enum.h"\n' % ns
        name = os.path.join(self.props["pj_path"], "common", "include", "%s.h" % ad_header_name)
        self.props["H_NAME"] = ad_header_name.upper()
        ctx = ad_template.format(**self.props)

        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

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
        name = os.path.join(self.props["pj_path"], "common", "include", "%s.h" % basebuilder.l_ns_name)
        self.props["h_name"] =basebuilder.l_ns_name
        self.props["H_NAME"] = basebuilder.l_ns_name.upper()
        self.props['deplist'] = self.deplist
        self.props['headers']=''
        for ns in self.GetNamespaces():
            self.props['headers'] += '#include "%s.h"\n\n' % ns

        ctx = local_header_template.format(**self.props)
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

        name = os.path.join(self.props["pj_path"], "common", "include", "%s_Depends.h" % basebuilder.l_ns_name)
        self.props["h_name"] =basebuilder.l_ns_name+ "_Depends"
        self.props["H_NAME"] =self.props["h_name"].upper()

        ctx = depends_template.format(**self.props)
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

    def BuildBegin(self):
        """ 构建准备，检查构建条件以及初始化 """
        
        if not os.path.isdir(self.folder):
            raise RuntimeError(u"folder(%s) is not exist!" % self.folder)

        self.elements = {}
        self.outfiles = []
        #append default XML namespace
    def Build(self):
        """开始构建 为每一个Namespace创建一个CPP头文件 """
        cipath = os.path.join(self.folder, "common", "include")
        if not os.path.exists(cipath):
            os.makedirs(cipath)

        #print self.GetNamespaces()
        self.depends={} #struct --> {struct}
        self.depvalue={}
        self.deplist=""
        self.dep_pod = {} #id --> 1/0

        self.props = {}
        self.props['local_ns_name'] = basebuilder.l_ns_name
        self.props['l_typedef'] = ad_header_name
        self.props["user_name"] = "LMiced Org"
        self.props['user_dept'] = 'Tsinghua'
        self.props["tm_now"] =time.strftime("%Y-%m-%d %H:%M:%S")
        self.props["pj_path"] =self.folder
        self.props["arraylist"]=''
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
                    #print "Array"
                    self.CreateArrayCPPHeader(item)
                elif item.item_type == "CompData":    #复合结构
                    #print "Comp data"
                    self.CreateCompCPPHeader(item)
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

        self.WriteLocalHeaderFile()


    def BuildEnd(self):
        """结束构建 关闭所有头文件 """
        '''for ns in self.elements:
            root = self.elements[ns]
            self.SaveNamespaceFile(ns, root)'''

    def GetFiles(self):
        return self.outfiles
