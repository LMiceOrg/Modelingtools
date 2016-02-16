$def with (ctx)
$ clsname = ''.join(('C', ctx['pj_name'], 'Impl') )

$ header = ''.join(('#include"', ctx["so_folder"], '.h"\n#include"', ctx['pj_name'], 'Impl.h"'))
$header

#define WIN32_MEAN_AND_LEAN
#include <Windows.h>
#include "Shlwapi.h"
#pragma comment(lib, "shlwapi.lib")

#include <math.h>

/**********************
 * 辅助函数
*********************/
static void setParameter(CParameterSet* paramSet, const wchar_t* propertyName, const void* data, int size ) {
    CParameter *param = new CParameter(propertyName);
    param->setStructValue(data, size);
    paramSet->addPar(param);
}

static bool getParameter( const CEventParameterSet* paramSet, const wchar_t* propertyName, AppSim::String &value )
{
    if(paramSet->isExist( propertyName ) )
    {
        value = (*paramSet)[propertyName]->getStringValue();
        return true;
    }
    return false;
}
static bool getParameter( const CParameterSet* paramSet, const wchar_t* propertyName, AppSim::String &value )
{
    if(paramSet->isExist( propertyName ) )
    {
        value = (*paramSet)[propertyName]->getStringValue();
        return true;
    }
    return false;
}

inline bool operator ==( const AppSim::Wstring255& w1, const AppSim::Wstring255& w2) {
    return wcscmp(w1.value, w2.value) == 0;
}

inline AppSim::Wstring255& operator<<(AppSim::Wstring255& w1, const AppSim::Wstring255& w2) {
    memcpy(w1.value, w2.value, sizeof(w1));
    return w1;
}

/**********************
 * 性能参数读取函数
*********************/
static void GetPerfWString(const wchar_t* file, const wchar_t* name, AppSim::Wstring255& value) {
    memset(value.value, 0, sizeof(value));
    GetPrivateProfileStringW(_T("perf"), name, _T(""), value.value, 255, file );
}

static void GetPerfWString(const wchar_t* file, const wchar_t* name, wchar_t* value, int size) {
    memset(value, 0, sizeof(wchar_t)*size);
    GetPrivateProfileStringW(_T("perf"), name, _T(""), value, size, file );
}

static void GetPerfWString(const wchar_t* file, const wchar_t* name, std::wstring& value) {
    wchar_t buff[512];
    memset(buff, 0, sizeof(buff));
    GetPrivateProfileStringW(_T("perf"), name, _T(""), buff, 511, file );
    value = buff;
}

template<class T>
static void GetPerfDouble(const wchar_t* file, const wchar_t* name, T& value) {
    wchar_t buff[512];
    memset(buff, 0, sizeof(buff));
    value = 0;
    GetPrivateProfileStringW(_T("perf"), name, 0, buff, 511, file );
    std::wstringstream ss;
    ss<<buff;
    ss>>value;
}

template<class T>
static void GetPerfInt(const wchar_t* file, const wchar_t* name, T& value) {
    value = 0;
    value = GetPrivateProfileIntW(_T("perf"), name, 0, file );
}


static void GetPerfBool(const wchar_t* file, const wchar_t* name, bool& value) {
    value = false;
    value = GetPrivateProfileIntW(_T("perf"), name, 0, file );
}

template< class T>
static void GetPerfVector(const wchar_t* file, const wchar_t* name, std::vector<T>& value) {
    wchar_t buff[512];
    memset(buff, 0, sizeof(buff));
    value.clear();
    GetPrivateProfileStringW(_T("perf"), name, 0, buff, 511, file );
    std::wstringstream ss(buff);

    T d;
    while(!ss.eof()) {
        ss>>d;
        ss.get();
        if(ss.eof())
           break;
        value.push_back(d);
    }
}

//枚举数组类型
template< class T>
static void GetPerfVectorEnum(const wchar_t* file, const wchar_t* name, std::vector<T>& value) {
    wchar_t buff[512];
    memset(buff, 0, sizeof(buff));
    value.clear();
    GetPrivateProfileStringW(_T("perf"), name, 0, buff, 511, file );
    std::wstringstream ss(buff);

    T d;
    int val;
    while(!ss.eof()) {
        ss>>val;
        ss.get();
        if(ss.eof())
           break;
        d=(T)val;
        value.push_back(d);
    }
}

/**********************
 * 公共基础类库导入
*********************/

pCalc_TrueAzimuth3 Calc_TrueAzimuth3 = NULL;
pCalc_TrueAzimuth2 Calc_TrueAzimuth2 = NULL;
pCalc_RelAzimuth Calc_RelAzimuth = NULL;
pCalc_Distance3 Calc_Distance3 = NULL;
pCalc_Distance2 Calc_Distance2 = NULL;
pCalc_IsBeamCover Calc_IsBeamCover = NULL;
pCalc_GeoVisionDis Calc_GeoVisionDis = NULL;
pCalc_TargetElevation3 Calc_TargetElevation3 = NULL;
pCalc_TargetElevation Calc_TargetElevation = NULL;
pCalc_TargetRelCourse Calc_TargetRelCourse = NULL;
pCalc_TargetRelSpeed Calc_TargetRelSpeed = NULL;
pCalc_DbmWToWatt Calc_DbmWToWatt = NULL;
pCalc_WattToDbmW Calc_WattToDbmW = NULL;
pCalc_WaveTransLoss Calc_WaveTransLoss = NULL;

//typedef void  (*pBLHtoXYZ) ( double B,double L,double H, double &X,double &Y,double &Z);
//typedef void  (*pXYZtoBLH) ( double X, double Y, double Z, double &B, double &L,double &H );

//typedef void  (*pMercator_SetB0L0) (double b0, double l0);
//typedef void  (*pMercator_xytoBL) (double x, double y, double& b, double& l);
//typedef void (*pMercator_BLtoxy) (double b, double l, double& x, double& y);

pMercator_SetB0L0 Mercator_SetB0L0 = NULL;
pMercator_xytoBL Mercator_xytoBL = NULL;
pMercator_BLtoxy Mercator_BLtoxy = NULL;


//void Calculate::LBHtoXYZ( const PosThreeDime_T& pos, PointThreeDime_T& point) {
//    BLHtoXYZ(pos.LAT, pos.LON, pos.Height, point.Y, point.X, point.Z);
//}


/**********************
 * 实现类
*********************/

$clsname::$clsname$'('$ctx["so_folder"] * obj)
:pobj(obj)
{
    /**************************** 获得公共基础算法函数 ****************************/

    HMODULE hModule = GetModuleHandleW(L"$ctx['so_folder']$'.dll'");
    wchar_t buff[512];
    GetModuleFileNameW(hModule, buff, 511);
    PathRemoveFileSpecW(buff);
    PathAppendW(buff, L"CoordinateTransfer.dll");
    HMODULE hmod = LoadLibraryW(buff);
    Mercator_SetB0L0 = (pMercator_SetB0L0)GetProcAddress(hmod, "Mercator_SetB0L0");
    Mercator_xytoBL = (pMercator_xytoBL)GetProcAddress(hmod, "Mercator_xytoBL");
    Mercator_BLtoxy = (pMercator_BLtoxy)GetProcAddress(hmod, "Mercator_BLtoxy");

    PathRemoveFileSpecW(buff);
    PathAppendW(buff, L"NTAlgorithm.dll");
    hmod = LoadLibraryW(buff);

    //计算目标点相对于基点的真方位
    Calc_TrueAzimuth3 = (pCalc_TrueAzimuth3)GetProcAddress(hmod, "Calc_TrueAzimuth3");
    Calc_TrueAzimuth2 = (pCalc_TrueAzimuth2)GetProcAddress(hmod, "Calc_TrueAzimuth2");

    //计算目标点相对于基础方向的相对方位
    Calc_RelAzimuth = (pCalc_RelAzimuth)GetProcAddress(hmod, "Calc_RelAzimuth");

    //计算两点之间的距离
    Calc_Distance3 = (pCalc_Distance3)GetProcAddress(hmod, "Calc_Distance3");
    Calc_Distance2 = (pCalc_Distance2)GetProcAddress(hmod, "Calc_Distance2");

    //计算目标点是否在从基点发出的锥体形波束的覆盖范围内
    Calc_IsBeamCover = (pCalc_IsBeamCover)GetProcAddress(hmod, "Calc_IsBeamCover");

    //计算两点之间的通视距离
    Calc_GeoVisionDis = (pCalc_GeoVisionDis)GetProcAddress(hmod, "Calc_GeoVisionDis");

    //计算目标点相对于基点的俯仰角【-90， 90】
    Calc_TargetElevation3 = (pCalc_TargetElevation3)GetProcAddress(hmod, "Calc_TargetElevation3");
    Calc_TargetElevation = (pCalc_TargetElevation)GetProcAddress(hmod, "Calc_TargetElevation");

    //计算目标点相对于基点的相对航向
    Calc_TargetRelCourse = (pCalc_TargetRelCourse)GetProcAddress(hmod, "Calc_TargetRelCourse");

    //计算目标点相对于基点的相对航速
    Calc_TargetRelSpeed = (pCalc_TargetRelSpeed)GetProcAddress(hmod, "Calc_TargetRelSpeed");

    //分贝毫瓦到瓦特的转换
    Calc_DbmWToWatt = (pCalc_DbmWToWatt)GetProcAddress(hmod, "Calc_DbmWToWatt");

    //瓦特到分贝毫瓦的转换
    Calc_WattToDbmW = (pCalc_WattToDbmW)GetProcAddress(hmod, "Calc_WattToDbmW");

    //大气传输衰减计算
    //频率Wave_Fre(MHz),距离Dis_Trans(m)
    Calc_WaveTransLoss = (pCalc_WaveTransLoss)GetProcAddress(hmod, "Calc_WaveTransLoss");

}

$clsname::~$clsname$'('void)
{
}

bool $clsname::init() {

    int enumValue = 0;
    std::wstring file;

    file = pobj->m_wstrCurrentPath + pobj->m_PerforFile.value;
    loginfo(pobj->m_Logger, _T("Read Performance")<< file );

$for item in ctx['perf_def']:
        /* name:$item.it_cname
         * desc:$item.it_desc
         */
    $if item.it_type in ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64']:
            GetPerfInt(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name = "<<m_$item.it_name);

    $elif item.it_type in ['Wstring255', 'Wstring']:
            GetPerfWString(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name = "<<toTString(m_$item.it_name) );

    $elif item.it_type in ['Float64', 'Float32']:
            GetPerfDouble(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name = "<<m_$item.it_name);

    $elif item.it_type in ['Bool']:
            GetPerfBool(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name = "<<m_$item.it_name);

    $elif item.it_type[:6] in ['vector'] and item.or_type[:5] not in ['Enum_']:
            GetPerfVector(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name size = "<<m_$item.it_name$'.size()');
            //for(size_t i=0; i < m_$item.it_name$'.size()'; ++i) {
            //    loginfo(pobj->m_Logger, L"$item.it_name$'["<<i<<L"]="<<'m_$item.it_name$'[i]');
            //}

    $elif item.it_type[:6] in ['vector'] and item.or_type[:5] in ['Enum_']:
            GetPerfVectorEnum(file.c_str(), L"$item.it_name", m_$item.it_name);
            loginfo(pobj->m_Logger, L"$item.it_name size = "<<m_$item.it_name$'.size()');
            //for(size_t i=0; i < m_$item.it_name$'.size()'; ++i) {
            //    loginfo(pobj->m_Logger, L"$item.it_name$'["<<i<<L"]='"<<(int)m_$item.it_name$'[i]');
            //}

    $else:
            GetPerfInt(file.c_str(), L"$item.it_name", enumValue);
            m_$item.it_name = ($item.it_type)enumValue;
            loginfo(pobj->m_Logger, L"$item.it_name = "<<m_$item.it_name);

$#

    return true;
}

void $clsname::input(const CParameterSet* paramSet) {
    loginfo(pobj->m_Logger, _T("$clsname input") );
    std::string value;

$for item in ctx['info_def']:
    $ info_type = '::'.join((RefineContext(item.cd_ns), item.cd_type))
    $if item.cd_io != u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
            if( getParameter(paramSet, L"$item.cd_name", value) ) {
                $info_type info;
                info.unpack(value.c_str(), value.size());
                for(size_t i=0; i<m_input_$item.cd_name$'.'size(); ++i) {
                    if( m_input_$item.cd_name$'[i].'Info_Basic.ID == info.Info_Basic.ID) {
                        m_input_$item.cd_name$'.'erase(m_input_$item.cd_name$'.'begin() + i);
                        break;
                    }
                }
                m_input_$item.cd_name$'.'push_back(info);
            }

$#
}

void $clsname::output(CParameterSet* paramSet) {
    loginfo(pobj->m_Logger, _T("$clsname output") );

$for item in ctx['info_def']:
    $ info_type = '::'.join((RefineContext(item.cd_ns), item.cd_type))
    $if item.cd_io == u'输出':
            if(m_output_$item.cd_name$'.'size() > 0) {
                const $info_type &info = m_output_$item.cd_name$'[0]';
                std::vector<char> data(info.size());
                info.pack(&data[0], data.size());
                setParameter(paramSet, L"$item.cd_name", &data[0], data.size());
            }

$#
}

void $clsname::receiveEvent(const CEventParameterSet* paramSet) {
    loginfo(pobj->m_Logger, _T("$clsname receiveEvent") );
    std::string value;

$for item in ctx['evts_def']:
    $ info_type = '::'.join((RefineContext(item.cd_ns), item.cd_type))
    $if item.cd_io != u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
            if( getParameter(paramSet, L"$item.cd_name", value) ) {
                $info_type evt;
                evt.unpack(value.c_str(), value.size());
                m_receive_$item.cd_name$'.'push_back(evt);
            }

$#
}

void $clsname::sendEvent(CEventParameterSet* paramSet, uint32 sendIndex) {
    loginfo(pobj->m_Logger, _T("$clsname sendEvent") );

}

LONGRESULT $clsname::run(CEE_Time_t simTime, CEE_Time_t dt) {
    loginfo(pobj->m_Logger, _T("$clsname run") );

    //在run函数开始时，清空上一次运行的输出信息

$for item in ctx['info_def']:
    $if item.cd_io == u'输出':
            m_output_$item.cd_name$'.'clear();

$#

    //在run函数开始时，清空上一次运行的输出事件

$for item in ctx['evts_def']:
    $if item.cd_io == u'输出':
            m_send_$item.cd_name$'.'clear();

$#

    /**************run 函数 自定义 流程 **************/






    //在run函数执行结束后，清空接收到的事件

$for item in ctx['evts_def']:
    $if item.cd_io != u'输出':
            m_receive_$item.cd_name$'.'clear();

$#

    return ComponentStatusCode::Running;
}
