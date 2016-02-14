#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  模块初始化文件

"""
import os

#默认工程路径
default_model_folder = 'e:/model'

#本地模型命名空间
l_ns_name = 'NTSim'
default_ns_key = '0_'
default_ns_name = "NTSim_Global"

#模型描述文件
model_decl_key = 'M3_'
#列表
nslist ={
'0_':["通用类","NTSim_Global", None],
'B_':["平台类","NTSim_Platform", None],
'C_':["传感器类","NTSim_Sensor", None],
'E_':["通信设备类","NTSim_Comm", None],
'G_':["干扰设备类","NTSim_Jam", None],
'F_':["武器类","NTSim_Weapon", None],
'D_':["指挥控制与数据处理设备类","NTSim_CCDP", None]
}



#外部代码生成工具
external_model_code_tools = '"C:/Program Files (x86)/appsoft/DWK/V32/SimDevStudio/ComponentDev/AppSimFom.exe" {model_folder} {model_folder}/../common/modeldesc/{so_folder}.xml 0 DWK false'

#命名空间映射关系
#在正式输出前根据映射关系进行替换
#将key命名空间替换为value命名空间
#此表为空则表示不作替换
namespace_refine_mapping ={"NTSim_Global":l_ns_name,
"NTSim_Platform":l_ns_name,
"NTSim_Sensor":l_ns_name,
"NTSim_Comm":l_ns_name,
"NTSim_Jam":l_ns_name,
"NTSim_Weapon":l_ns_name,
"NTSim_CCDP":l_ns_name

}

#生成的数据描述XML命名空间
l_xmlns_datastructs={
'xmlns:Types':"http://www.appsoft.com.cn/Core/Types",
"xmlns:xlink":"http://www.w3.org/1999/xlink",
"xsi:schemaLocation":"http://www.appsoft.com.cn/Core/Catalogue Core/Catalogue.xsd",
"xmlns:Catalogue":"http://www.appsoft.com.cn/Core/Catalogue",
"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
}

l_xmlns_modeldescs={
"xmlns:Types":"http://www.appsoft.com.cn/Core/Types",
"xsi:schemaLocation":"http://www.appsoft.com.cn/Component ../Component.xsd",
"xmlns:Component":"http://www.appsoft.com.cn/Component",
"xmlns:xlink":"http://www.w3.org/1999/xlink",
"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"
}

#全局类型命名空间
g_ns_name = "AppSim"
g_ns_type_mapping = {
'double':('Float64', g_ns_name,'0'),
'float':('Float32',g_ns_name,'0'),

'wchar_t':('Wchar', g_ns_name,"'\\0'"),
'char':('Char', g_ns_name ,"'\\0'"),
'unsigned char':('UChar', g_ns_name ,"'\\0'"),

'std::string':('String', g_ns_name ,None),
'std::wstring':('Wstring', g_ns_name ,None),

'bool':('Bool',g_ns_name, 'false'),

'int8_t':('Int8',g_ns_name, '0'),
'int16_t':('Int16',g_ns_name, '0'),
'int32_t':('Int32',g_ns_name, '0'),
'int64_t':('Int64',g_ns_name, '0'),
'short':('Int16',g_ns_name, '0'),
'int':('Int32',g_ns_name, '0'),



'uint8_t':('UInt8',g_ns_name, '0'),
'uint16_t':('UInt16',g_ns_name, '0'),
'uint32_t':('UInt32',g_ns_name, '0'),
'uint64_t':('UInt64',g_ns_name, '0'),
'unsigned short':('UInt16',g_ns_name, '0'),
'unsigned int':('UInt32',g_ns_name, '0')


}

# 数据类型映射关系表
dt_mapping = dict(g_ns_type_mapping)
dt_mapping['doubel'] = g_ns_type_mapping['double']
dt_mapping['string'] = g_ns_type_mapping['std::string']
dt_mapping['wstring'] = g_ns_type_mapping['std::wstring']

dt_mapping['char[256]'] = ('String256', 'NTSim_Global', None)
dt_mapping['char[128]'] = ('String128', 'NTSim_Global', None)
dt_mapping['char[64]'] = ('String64', 'NTSim_Global', None)
dt_mapping['char[32]'] = ('String32', 'NTSim_Global', None)
dt_mapping['char[24]'] = ('String24', 'NTSim_Global', None)

dt_mapping['long long'] = ('Int64',g_ns_name, '0')
dt_mapping['unsigned long long'] =('UInt64',g_ns_name, '0')
dt_mapping['signed char'] = ('Char', g_ns_name, '0')
dt_mapping['unsigned long'] = ('UInt64',g_ns_name, '0')
dt_mapping['long'] = ('Int64', g_ns_name, '0')

def gen_g_ns_type():
    s = {}
    for k in g_ns_type_mapping:
        key = g_ns_type_mapping[k]
        if not s.has_key( key ):
            s[ key ] = k
    return s



simapp_dtfile = os.path.split(os.path.abspath(__file__))[0]+"/builder/AppSim_Types.xml"

#生成文件的encoding设置
file_encode_default='utf-8'
file_encode_mapping_={
".xml":"utf-8",
".dsc":"utf-8",
".h":"gbk",
".cpp":'gbk',
'.ini':'utf-8'
}

__all__=['default_ns_key', 'default_ns_name', 'dt_mapping', 'nslist', 'g_ns_name', 'gen_g_ns_type', 'simapp_dtfile', 'l_ns_name', 'model_decl_key', 'l_xmlns_datastructs', 'l_xmlns_modeldescs', 'external_model_code_tools', 'namespace_refine_mapping', 'default_model_folder']
