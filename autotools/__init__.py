#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  模块初始化文件

"""
import os

default_ns_key = '0_'
default_ns_name = "NTSim_Global"

# 数据类型映射关系表
dt_mapping = {
'double':('Float64', 'AppSim'),
'float':('Float32','AppSim'),
'long':('Int64','AppSim'),
'string':('String', 'AppSim'),
'bool':('Bool','AppSim'),
'char[128]':('String128', 'NTSim_Global'),
'char[32]':('String32', 'NTSim_Global'),
'char[24]':('String24', 'NTSim_Global'),
'int':('Int32','AppSim')
}

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

simapp_dtfile = os.path.split(os.path.abspath(__file__))[0]+"/AppSim_Types.xml"
__all__=['default_ns_key', 'default_ns_name', 'dt_mapping', 'simapp_dtfile', 'nslist']
