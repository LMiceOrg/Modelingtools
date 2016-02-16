#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  msvc2008项目文件生成

在构造Project前，首先构造Solution,并将props参数传递给此类
"""

import os
import xml.etree.cElementTree as xmllib
import xml.dom.minidom as minidom
import web.template
import basebuilder

render = web.template.render(os.path.split(os.path.realpath(__file__))[0],
globals={'type':type,"hasattr":hasattr})


h_userdata_template = u"""#ifndef {PJ_NAME}_USERDATATYPE_H_
#define {PJ_NAME}_USERDATATYPE_H_
#include <AppSimKernel.h>
using namespace AppSim;

// NTSim global type definition
#include "../../../common/include/NTSim.h"

// {pj_name} private type definition

using namespace NTSim;

#include <map>
#include <string>
#include <vector>
using std::string;
using std::vector;
using std::map;


#endif /** {PJ_NAME}_USERDATATYPE_H_ */

"""

h_export_template=u"""#ifndef {PJ_NAME}_EXPORT_H_
#define {PJ_NAME}_EXPORT_H_
#if defined(_WIN32)
        #pragma warning(disable: 4251)
        #if defined({PJ_NAME}_EXPORTS)
                #define {PJ_NAME}_API __declspec(dllexport)
        #else
                #define {PJ_NAME}_API __declspec(dllimport)
        #endif
#else
        #define {PJ_NAME}_API
#endif

#endif /** {PJ_NAME}_EXPORT_H_ */

"""

h_template=u"""
/****************************************************************************
**
**	开发单位：Dist3
**	开发者：hehao
**	创建时间：{tm_now}
**	版本号：V1.0
**	描述信息：{pj_cname}
****************************************************************************/
#ifndef {PJ_NAME}_H_
#define {PJ_NAME}_H_
#include <AppSimKernel.h>
#include <ModelComponent.h>
#include "{PJ_NAME}Export.h"
#include "{PJ_NAME}UserDataType.h"
//#include "/Users/hehao/work/modelingtools/modelinitparser.h"

using namespace AppSimCEE;
using namespace AppSimCEE::Model;

/**
*@brief {pj_cname} 模型组件
* 模型构建自 {src_path}
*
*/
class {PJ_NAME}_API {pj_name} : public IModelComponent
{{
        AppSimCEE::Logger m_Logger;
public:
        /**
        *@brief 组件构造函数
        */
        {pj_name}(void);

        /**
        *@brief 组件析构函数
        */
        virtual ~{pj_name}(void);

        /**
        *@brief 组件初始化
        *@paramparamSet 组件初始化数据属性集
        */
        virtual bool init(const CParameterSet* paramSet);

        /**
        *@brief 组件输入接口
        *@param paramSet 组件输入接口数据属性集
        */
        virtual void input(const CParameterSet* paramSet);

        /**
        *@brief 组件输出接口
        *@param paramSet 组件输出接口数据属性集
        */
        virtual void output(CParameterSet* paramSet);

        /**
        *@brief 组件接收事件接口
        *@param paramSet 组件接收事件数据属性集
        */
        virtual void receiveEvent(const CEventParameterSet* paramSet);

        /**
        *@brief 组件发送事件接口
        *@param paramSet 组件发送事件数据属性集
        *@param sendIndex 当前发送的次数(从0开始的数字)
        */
        virtual void sendEvent(CEventParameterSet* paramSet, uint32 sendIndex);

        /**
        *@brief 组件运行接口
        *@param simTime 组件运行仿真时间
        *@param dt 组件运行仿真步长
        *@return 组件运行状态码
        */
        virtual LONGRESULT run(CEE_Time_t simTime, CEE_Time_t dt);

        /**
        *@brief 组件状态保存接口
        *@param paramSet 要保存的属性信息(名称，值)集合
        *@return void
        */
        virtual void save(CParameterSet* paramSet);

        /**
        *@brief 组件状态恢复接口
        *@param paramSet 要恢复的属性信息(名称，值)集合
        *@return void
        */
        virtual void restore(const CParameterSet* paramSet);

        /**
        *@brief 设置组件调试级别接口
        *@param level 调试级别
        *@return void
        */
         virtual void setDebugLevel(LogLevel level);

        /**
        *@brief 记录用户自定义分析数据接口
        *@param paramSet 分析数据属性集
        *@return void
        */
        virtual void recordAnalysisData(CParameterSet* paramSet);

        /**
        *@brief 获得需要发送事件的次数
        *@return uint32
        */
        virtual uint32 getEventCount();

        /**
        *@brief 引擎状态发生变化时触发的事件
        *@param statusCode 引擎状态
        *@return void
        */
        virtual void onEngineStatusCodeChanged(AppSimCEE::Model::EngineStatusCode statusCode);

        /**
        *@brief 退出仿真
        *@		调用时机:引擎退出运行时
        *@return void
        */
        virtual void exitSimulation();

protected:
        // TODO：用户自定义变量

private:

        {pj_initparam}
}};

/**
*@brief 创建组件实例接口
*/
extern "C" {PJ_NAME}_API  IComponent* create();

#endif //{PJ_NAME}_H_
"""

cpp_template=u"""
#include "{pj_name}.h"
IComponent* create()
{{
        IComponent* {pj_name}Instance = new {pj_name}();
        return {pj_name}Instance;
}}

/**
*@brief 组件构造函数
*/
{pj_name}::{pj_name}(void)
{{
        //自定义变量初始化

        //变量初始化
        m_Camp = 0;//敌我属性
        m_Altitude = 0;//高度
        m_Pitch = 0;//天线仰角
        m_AntennalModel = (KZY_DATASPACE::Enum_AtennalModel)0;//天线模式（分为全向和定向两种）
        m_BandWidth = 0;//信号带宽[10^(-1),10^5]
        m_CentralFrequency = 0;//中心频率[10^(-1),10^5]
        m_EquipmentID = 0;//装备型号(唯一标识)
        m_EquipmentType = L"";//装备类型
        memset(&m_FormationName, 0, sizeof(AppSim::Wstring255));//编队名称
        m_FormationID = 0;//编队ID
        m_IsTurnOn = false;//雷达开关机状态（缺省一直开机）
        m_Latitude = 0;//纬度
        m_Longitude = 0;//经度
        m_MainGain = 0;//主瓣增益[-10^4,10^4]
        m_NoiseFigure = 0;//噪声系数
        m_PolaType = (KZY_DATASPACE::Enum_RadarPolarType)0;//极化方式HH、HV、VH、VV、圆极化
        m_RadarSwitchTime = 0;//雷达开机时间(5分钟，[0-100])
        m_RequiredSNR = 0;//设备需要的最小信噪比
        m_ScanningTime = 0;//雷达扫描周期（秒）
        m_TransmitterPower = 0;//发射功率[10^(-6),10^6]

        //设置日志输出的位置,到文件{PJ_NAME}.log
        //m_Logger.setLogWriter(new AppSimCEE::FileLogWriter(L"{PJ_NAME}.log"));

        //设置日志输出的位置,到控制台
        m_Logger.setLogWriter(new AppSimCEE::DefaultLogWriter());

        //设置日志等级
        m_Logger.setLogging(ALL_LOG_LEVEL);

}}

/**
*@brief 组件析构函数
*/
{pj_name}::~{pj_name}(void)
{{

}}

/**
*@brief 组件初始化
*@paramparamSet 组件初始化数据属性集
*/
bool {pj_name}::init(const CParameterSet* paramSet)
{{
        //属性初始化
        if(paramSet->isExist(L"Camp"))
        {{
                m_Camp = (*paramSet)[L"Camp"]->getInt32Value();
        }}

        if(paramSet->isExist(L"Altitude"))
        {{
                m_Altitude = (*paramSet)[L"Altitude"]->getFloat32Value();
        }}

        if(paramSet->isExist(L"Pitch"))
        {{
                m_Pitch = (*paramSet)[L"Pitch"]->getFloat32Value();
        }}

        if(paramSet->isExist(L"AntennalModel"))
        {{
                int nSize = (*paramSet)[L"AntennalModel"]->size();
                memcpy( &m_AntennalModel, (*paramSet)[_T("AntennalModel")]->buffer(0), nSize );
        }}

        if(paramSet->isExist(L"BandWidth"))
        {{
                m_BandWidth = (*paramSet)[L"BandWidth"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"CentralFrequency"))
        {{
                m_CentralFrequency = (*paramSet)[L"CentralFrequency"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"EquipmentID"))
        {{
                m_EquipmentID = (*paramSet)[L"EquipmentID"]->getInt32Value();
        }}

        if(paramSet->isExist(L"EquipmentType"))
        {{
                m_EquipmentType = (*paramSet)[L"EquipmentType"]->getWstringValue();
        }}

        if(paramSet->isExist(L"FormationName"))
        {{
                (*paramSet)[L"FormationName"]->getWString255Value(m_FormationName);
        }}

        if(paramSet->isExist(L"FormationID"))
        {{
                m_FormationID = (*paramSet)[L"FormationID"]->getInt32Value();
        }}

        if(paramSet->isExist(L"IsTurnOn"))
        {{
                m_IsTurnOn = (*paramSet)[L"IsTurnOn"]->getBoolValue();
        }}

        if(paramSet->isExist(L"Latitude"))
        {{
                m_Latitude = (*paramSet)[L"Latitude"]->getFloat32Value();
        }}

        if(paramSet->isExist(L"Longitude"))
        {{
                m_Longitude = (*paramSet)[L"Longitude"]->getFloat32Value();
        }}

        if(paramSet->isExist(L"MainGain"))
        {{
                m_MainGain = (*paramSet)[L"MainGain"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"NoiseFigure"))
        {{
                m_NoiseFigure = (*paramSet)[L"NoiseFigure"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"PolaType"))
        {{
                int nSize = (*paramSet)[L"PolaType"]->size();
                memcpy( &m_PolaType, (*paramSet)[_T("PolaType")]->buffer(0), nSize );
        }}

        if(paramSet->isExist(L"RadarSwitchTime"))
        {{
                m_RadarSwitchTime = (*paramSet)[L"RadarSwitchTime"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"RequiredSNR"))
        {{
                m_RequiredSNR = (*paramSet)[L"RequiredSNR"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"ScanningTime"))
        {{
                m_ScanningTime = (*paramSet)[L"ScanningTime"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"TransmitterPower"))
        {{
                m_TransmitterPower = (*paramSet)[L"TransmitterPower"]->getFloat64Value();
        }}

        //性能参数初始化
        ModelInit();

        return true;
}}

/**
*@brief 组件输入接口
*@param paramSet 组件输入接口数据属性集
*/
void {pj_name}::input(const CParameterSet* paramSet)
{{
        //TODO 在此处添加本组件的输入处理

        Wstring input_Object_FormationCombinationInfo;
        Float64 input_Altitude;
        Float64 input_Latitude;
        Float64 input_Longitude;
        if(paramSet->isExist(L"Object_FormationCombinationInfo"))
        {{
                input_Object_FormationCombinationInfo = (*paramSet)[L"Object_FormationCombinationInfo"]->getWstringValue();
        }}

        if(paramSet->isExist(L"Altitude"))
        {{
                input_Altitude = (*paramSet)[L"Altitude"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"Latitude"))
        {{
                input_Latitude = (*paramSet)[L"Latitude"]->getFloat64Value();
        }}

        if(paramSet->isExist(L"Longitude"))
        {{
                input_Longitude = (*paramSet)[L"Longitude"]->getFloat64Value();
        }}

}}

/**
*@brief 组件输出接口
*@param paramSet 组件输出接口数据属性集
*/
void {pj_name}::output(CParameterSet* paramSet)
{{
        //TODO 在此处添加本组件的输出处理
        /*例如：
        CParameter*  px = new CParameter(L"Name");
        px->setStringValue("TestValue");
        paramSet->addPar(px);
        */

}}

/**
*@brief 组件接收事件接口
*@param paramSet 组件接收事件数据属性集
*/
void {pj_name}::receiveEvent(const CEventParameterSet* paramSet)
{{
        //TODO 在此处添加本组件的事件接收处理
        Wstring input_Event_RadarInterfereBegin;
        Wstring input_Event_RadarInterfereEnd;
        Wstring input_Command_RadarSwitch;
        if(paramSet->isExist(L"Event_RadarInterfereBegin"))
        {{
                input_Event_RadarInterfereBegin = (*paramSet)[L"Event_RadarInterfereBegin"]->getWstringValue();
        }}
        if(paramSet->isExist(L"Event_RadarInterfereEnd"))
        {{
                input_Event_RadarInterfereEnd = (*paramSet)[L"Event_RadarInterfereEnd"]->getWstringValue();
        }}
        if(paramSet->isExist(L"Command_RadarSwitch"))
        {{
                input_Command_RadarSwitch = (*paramSet)[L"Command_RadarSwitch"]->getWstringValue();
        }}
}}

/**
*@brief 组件发送事件接口
*@param paramSet 组件发送事件数据属性集
*@param sendIndex 当前发送的次数(从0开始的数字)
*/
void {pj_name}::sendEvent(CEventParameterSet* paramSet, uint32 sendIndex)
{{
        //TODO 在此处添加本组件的事件发送处理
        /*例如：
        CParameter*  px = new CParameter(L"Name");
        px->setStringValue("TestSendEventValue");
        paramSet->addPar(px);
        */

}}

/**
*@brief 组件运行接口
*@param simTime 组件运行仿真时间
*@param dt 组件运行仿真步长
*@return 组件运行状态码
*/
LONGRESULT {pj_name}::run(CEE_Time_t simTime, CEE_Time_t dt)
{{
        //TODO 在此处添加本组件的运行处理

        return ComponentStatusCode::Running;
}}

/**
*@brief 组件状态保存接口
*@param paramSet 要保存的属性信息(名称，值)集合
*@return void
*/
void {pj_name}::save(CParameterSet* paramSet)
{{
        //TODO 用户自定义保存属性
        /*例如：
        CParameter*  px = new CParameter(L"Name");
        px->setStringValue(Name);
        paramSet->addPar(px);
        */

}}

/**
*@brief 组件状态恢复接口
*@param paramSet 要恢复的属性信息(名称，值)集合
*@return void
*/
void {pj_name}::restore(const CParameterSet* paramSet)
{{
        //TODO 用户自定义组件恢复运行操作
        /*例如：
        if(paramSet->isExist(L"Name"))
        {{
                name = (*paramSet)[L"Name"]->stringValue();
        }}*/

}}

/**
*@brief 设置组件调试级别接口
*@param level 调试级别
*@return void
*/
void {pj_name}::setDebugLevel(LogLevel level)
{{
        //设置调试等级
        m_Logger.setLogging(level);
}}

/**
*@brief 记录用户自定义分析数据接口
*@param paramSet 分析数据属性集
*@return void
*/
void {pj_name}::recordAnalysisData(CParameterSet* paramSet)
{{
        //TODO 用户自定义选择参数作为分析数据
        //自定义分析数据举例
        //输出标识为name的数据
        /*
        CParameter* parameter = new CParameter(_T("name"));
        parameter->setStringValue ("test");
        paramSet->addPar(parameter);*/

}}

/**
*@brief 获得需要发送事件的次数
*@return uint32
*/
uint32 {pj_name}::getEventCount()
{{
        int eventCount = 0;
        //TODO 用户需要自行处理需要调用的发送事件次数

        return eventCount;
}}

/**
*@brief 引擎状态发生变化时触发的事件
*@param statusCode 引擎状态
*@return void
*/
void {pj_name}::onEngineStatusCodeChanged(AppSimCEE::Model::EngineStatusCode statusCode)
{{
        switch(statusCode)
        {{
        case EngineStatusCode::RUNNING:
                {{
                // TODO: 用户处理RUNNING状态

                }}
                break;
        case EngineStatusCode::PAUSE:
                {{
                // TODO：用户处理PAUSE状态

                }}
                break;
        default:
                {{
                // TODO：用户处理默认状态

                }}
                break;
        }}
}}
/**
*@brief 退出仿真
*@		调用时机:引擎退出运行时
*@return void
*/
void {pj_name}::exitSimulation()
{{
        // TODO：退出仿真运行时，用户处理
}}

"""

class Msvc2008ProjectBuilder(object):
    def __init__(self):
        self.outfiles = []
    def BuildUserDataHeaderFile(self, props = None):
        if props == None:
            props = self.props
        bd = basebuilder.BaseBuilder(None)
        render._add_global(bd.RefineContext, 'RefineContext')
        #Update 接口类h
        name = os.path.join(props["pj_path"], "%s.h" % props["so_folder"])
        if os.path.isfile(name):
            f = open(name, 'r')
            ctx = f.read()
            f.close()
            #print ctx.find('private:')
            new_item = u"""private:
    //在接口类添加实现类的成员变量
    friend class C%sImpl;
    C%sImpl* pmodel;
                """ % (props['pj_name'], props['pj_name'])
            ctx = ctx.replace('private:',  new_item.encode('gbk'))
            f = open(name, 'w')
            f.write(ctx)
            f.close()

        #Update 接口类cpp
        name = os.path.join(props["pj_path"], "%s.cpp" % props["so_folder"])
        if os.path.isfile(name):
            f = open(name, 'r')
            ctx = f.read()
            f.close()

            #ctx = '#include "%sImpl.h"\n' % props['pj_name'].encode('gbk') + ctx
            ctx = ctx.replace('#include <Windows.h>\n', '#include <Windows.h>\n\n#include "%sImpl.h"\n\n' % props['pj_name'].encode('gbk') )
            new_item = u"""%s::%s(void)
{
    pmodel = new C%sImpl(this);""" % (props["so_folder"], props["so_folder"], props['pj_name'])
            ctx = ctx.replace('%s::%s(void)\n{' % (props["so_folder"].encode('gbk') , props["so_folder"].encode('gbk')) , new_item.encode('gbk'))
            f = open(name, 'w')
            f.write(ctx)
            f.close()

        #UserDefine hpp
        ctx = render.ud_hpp_tmpl(props)
        ctx = str(ctx)
        #ctx = h_userdata_template.format(** props)
        name = os.path.join(props["pj_path"], "%suserdatatype.h" % props["so_folder"])
        f=open(name, "w")
        #f.write( ctx.encode('utf-8') )
        f.write(ctx)
        f.close()
        self.outfiles.append(name)

        ctx = render.impl_hpp_tmpl(props)
        ctx = str(ctx)
        name = os.path.join(props["pj_path"], "%sImpl.h" % props["pj_name"])
        f=open(name, "w")
        f.write(ctx)
        f.close()
        self.outfiles.append(name)

        ctx = render.impl_cpp_tmpl(props)
        ctx = str(ctx)
        name = os.path.join(props["pj_path"], "%sImpl.cpp" % props["pj_name"])
        f=open(name, "w")
        #Utf-8 BOM
        f.write('\xef\xbb\xbf')
        f.write(ctx)
        f.close()
        self.outfiles.append(name)

    def BuildHeaderFile(self):
        self.props["pj_initparam"]=""
        ctx = h_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "%s.h" % self.props["pj_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

        self.BuildUserDataHeaderFile()

        ctx = h_export_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "%sexport.h" % self.props["pj_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

    def BuildCppFile(self):
        ctx = cpp_template.format(** self.props)
        name = os.path.join(self.props["pj_path"], "%s.cpp" % self.props["pj_name"])
        f=open(name, "w")
        f.write( ctx.encode('utf-8') )
        f.close()
        self.outfiles.append(name)

    def BuildConfiguration(self, root, cfg_type):
        node = xmllib.SubElement(root, "Configuration", {"Name":"%s|Win32" % cfg_type,
        "OutputDirectory":"$(SolutionDir)$(ConfigurationName)",
        "IntermediateDirectory":"$(ConfigurationName)",
        "ConfigurationType":"2",
        "CharacterSet":"1"})

        cc_flags={}
        ld_flags={}

        if cfg_type == "Debug":

            cc_flags["Optimization"] = "0"
            cc_flags['PreprocessorDefinitions'] = "WIN32;_DEBUG;_WINDOWS;_USRDLL;%s_EXPORTS" % self.props["pj_name"].upper()
            cc_flags['RuntimeLibrary']="3"
            cc_flags['DebugInformationFormat']='4'

            ld_flags['AdditionalDependencies']='AppSimd.lib'
            ld_flags['LinkIncremental']="2"

        elif cfg_type == "Release":
            node.set('WholeProgramOptimization','1')

            cc_flags["Optimization"] = "2"
            cc_flags['PreprocessorDefinitions'] = "WIN32;NDEBUG;_WINDOWS;_USRDLL;%s_EXPORTS" % self.props["pj_name"].upper()
            cc_flags['EnableIntrinsicFunctions']="true"
            cc_flags['RuntimeLibrary']="2"
            cc_flags['DebugInformationFormat']='3'

            ld_flags['AdditionalDependencies']='AppSim.lib'
            ld_flags['LinkIncremental']="1"
            ld_flags['OptimizeReferences']="2"
            ld_flags['EnableCOMDATFolding']="2"


        xmllib.SubElement(node, "Tool", {"Name":"VCPreBuildEventTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCCustomBuildTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCXMLDataGeneratorTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCWebServiceProxyGeneratorTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCMIDLTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCCLCompilerTool",
        'AdditionalIncludeDirectories':"\"$(DTS_CEE_DIR)\include\";\"$(SolutionDir)include\"",
        'MinimalRebuild':"true",
        'BasicRuntimeChecks':"3",
        'UsePrecompiledHeader':"0",
        'WarningLevel':"3"}, **cc_flags)
        xmllib.SubElement(node, "Tool", {"Name":"VCManagedResourceCompilerTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCResourceCompilerTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCPreLinkEventTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCLinkerTool",
        'OutputFile':"$(OutDir)\$(ProjectName).dll",
        'AdditionalLibraryDirectories':"\"$(DTS_CEE_DIR)\lib\"",
        'GenerateDebugInformation':"true",
        'SubSystem':"2",
        'TargetMachine':"1"}, **ld_flags)
        xmllib.SubElement(node, "Tool", {"Name":"VCALinkTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCManifestTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCXDCMakeTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCBscMakeTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCFxCopTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCAppVerifierTool"})
        xmllib.SubElement(node, "Tool", {"Name":"VCPostBuildEventTool",
        'CommandLine':"cd ..\n\"$(SolutionDir)pack.bat\" %s" % cfg_type})

    def BuildFilesNode(self, root):
        node = xmllib.SubElement(root, "Filter", {"Name":"源文件".decode('utf-8'),
        'Filter':"cpp;c;cc;cxx;def;odl;idl;hpj;bat;asm;asmx",
        'UniqueIdentifier':"{B81E32B6-F518-4FA6-B93E-C16C24A0B589}"})
        xmllib.SubElement(node, "File", {"RelativePath":".\\%s.cpp" % self.props['pj_name'] }).text = " "

        #2 Headers
        node = xmllib.SubElement(root, "Filter", {"Name":"头文件".decode('utf-8'),
        'Filter':"h;hpp;hxx;hm;inl;inc;xsd",
        'UniqueIdentifier':"{8D23DA25-D545-4EE4-A8F4-2B5FC406E6B0}"})
        xmllib.SubElement(node, "File", {"RelativePath":".\\%s.h" % self.props['pj_name'] }).text = " "
        xmllib.SubElement(node, "File", {"RelativePath":".\\%sExport.h" % self.props['pj_name'] }).text = " "
        xmllib.SubElement(node, "File", {"RelativePath":".\\%sUserDataType.h" % self.props['pj_name'] }).text = " "

    def BuildProject(self, props = None, tp = ""):
        self.outfiles = []
        if props != None:
            self.props = props

        root = xmllib.Element("VisualStudioProject", {"ProjectType":"Visual C++",
        "Version":"9.00",
        "Name":self.props["pj_name"],
        "ProjectGUID":"{%s}" % self.props["pj_uuid"],
        "RootNamespace":self.props["pj_name"],
        "Keyword":"Win32Proj",
        "TargetFrameworkVersion":"196613"})

        node = xmllib.SubElement(root, "Platforms")
        xmllib.SubElement(node, "Platform", {"Name":"Win32"})

        xmllib.SubElement(root, "ToolFiles").text=" "

        node = xmllib.SubElement(root, "Configurations")
        self.BuildConfiguration(node, "Debug")
        self.BuildConfiguration(node, "Release")

        xmllib.SubElement(root, "References").text = " "

        node = xmllib.SubElement(root, "Files")
        self.BuildFilesNode(node)

        xmllib.SubElement(root, "Globals").text = " "

        doc = minidom.parseString( xmllib.tostring(root, 'utf-8').replace('&#10;', 'code_new_line') )
        data = doc.toprettyxml(encoding="utf-8").replace('code_new_line', '&#x0D;&#x0A;')
        name = os.path.join(self.props["pj_path"], "%s.vcproj" % self.props["pj_name"])

        f = open(name, "w")
        f.write(data)
        f.close()
        self.outfiles.append(name)

        #Header files
        self.BuildHeaderFile()

        #Cpp file
        self.BuildCppFile()

        return self.outfiles
