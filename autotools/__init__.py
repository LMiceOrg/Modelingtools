#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  模块初始化文件

"""
import os

l_ns_name = 'NTSim'
default_ns_key = '0_'
default_ns_name = "NTSim_Global"

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


#全局类型命名空间
g_ns_name = "RealTimeLibrary"
g_ns_type_mapping = {
'double':('Float64', g_ns_name),
'float':('Float32',g_ns_name),

'wchar_t':('Wchar', g_ns_name),
'char':('Char', g_ns_name),
'unsigned char':('UChar', g_ns_name),

'std::string':('String', g_ns_name),
'std::wstring':('Wstring', g_ns_name),

'bool':('Bool',g_ns_name),

'int8_t':('Int8',g_ns_name),
'int16_t':('Int16',g_ns_name),
'int32_t':('Int32',g_ns_name),
'int64_t':('Int64',g_ns_name),
'short':('Int16',g_ns_name),
'int':('Int32',g_ns_name),



'uint8_t':('UInt8',g_ns_name),
'uint16_t':('UInt16',g_ns_name),
'uint32_t':('UInt32',g_ns_name),
'uint64_t':('UInt64',g_ns_name),
'unsigned short':('UInt16',g_ns_name),
'unsigned int':('UInt32',g_ns_name)


}

# 数据类型映射关系表
dt_mapping = dict(g_ns_type_mapping)
dt_mapping['doubel'] = g_ns_type_mapping['double']
dt_mapping['string'] = g_ns_type_mapping['std::string']
dt_mapping['wstring'] = g_ns_type_mapping['std::wstring']

dt_mapping['char[256]'] = ('String256', 'NTSim_Global')
dt_mapping['char[128]'] = ('String128', 'NTSim_Global')
dt_mapping['char[32]'] = ('String32', 'NTSim_Global')
dt_mapping['char[24]'] = ('String24', 'NTSim_Global')

dt_mapping['long long'] = ('Int64',g_ns_name)
dt_mapping['unsigned long long'] =('UInt64',g_ns_name)
dt_mapping['signed char'] = ('Char', g_ns_name)
dt_mapping['unsigned long'] = ('UInt64',g_ns_name)
dt_mapping['long'] = ('Int64', g_ns_name)

def gen_g_ns_type():
    s = {}
    for k in g_ns_type_mapping:
        key = g_ns_type_mapping[k]
        if not s.has_key( key ):
            s[ key ] = k
    return s


simapp_dtfile = os.path.split(os.path.abspath(__file__))[0]+"/builder/AppSim_Types.xml"
__all__=['default_ns_key', 'default_ns_name', 'dt_mapping', 'nslist', 'g_ns_name', 'gen_g_ns_type', 'simapp_dtfile', 'l_ns_name']
