$def with (ctx)
$ clsname = ''.join(('C', ctx['pj_name'], 'Impl'))
#ifndef $ctx['PJ_NAME']_IMPL_HPP_TMPL_H
#define $ctx['PJ_NAME']_IMPL_HPP_TMPL_H

/**************************** 公共基础算法 ****************************/
typedef void  (*pMercator_SetB0L0) (double b0, double l0);
typedef void  (*pMercator_xytoBL)  (double x, double y, double& b, double& l);
typedef void  (*pMercator_BLtoxy)  (double b, double l, double& x, double& y);

extern pMercator_SetB0L0 Mercator_SetB0L0;
extern pMercator_xytoBL Mercator_xytoBL;
extern pMercator_BLtoxy Mercator_BLtoxy;

#define Mercator_SetL0B0(pos) Mercator_SetB0L0(pos.LAT, pos.LON)
#define Mercator_XYtoLB(pt, pos) Mercator_xytoBL(pt.Y, pt.X, pos.LAT, pos.LON)
#define Mercator_LBtoXY(pos, pt) Mercator_BLtoxy(pos.LAT, pos.LON, pt.Y, pt.X)

typedef void  (*pBLHtoXYZ) ( double B,double L,double H, double &X,double &Y,double &Z);
typedef void (*pXYZtoBLH)( double X, double Y, double Z, double &B, double &L,double &H );

extern pBLHtoXYZ BLHtoXYZ;
extern pXYZtoBLH XYZtoBLH;


#define SurfaceXYZtoCoreXYZ(pts, ptc) do {$'\\'
    PosThreeDime_T pos; $'\\'
    pos.clear();    $'\\'
    Mercator_XYtoLB(pts, pos);  $'\\'
    pos.Height = pts.Height;    $'\\'
    BLHtoXYZ(pos.LAT, pos.LON, pos.Height, ptc.X, ptc.Y, ptc.Z);    $'\\'
    } while(0)  $'\\'

#define CoreXYZtoSurfaceXYZ(ptc, pts) do { $'\\'
    PosThreeDime_T pos;  $'\\'
    pos.clear();     $'\\'
    XYZtoBLH(ptc.X, ptc.Y, ptc.Z, pos.LAT, pos.LON, pos.Height);     $'\\'
    Mercator_LBtoXY(pos, pts);   $'\\'
    pts.Height = pos.Height;     $'\\'
    } while(0)   $'\\'


//计算目标点相对于基点的真方位
typedef void (*pCalc_TrueAzimuth3)(const PointThreeDime_T tar, const PointThreeDime_T base, double* ang);
extern pCalc_TrueAzimuth3 Calc_TrueAzimuth3;

typedef void (*pCalc_TrueAzimuth2)(const PointTwoDime_T tar , const PointTwoDime_T base, double* ang);
extern pCalc_TrueAzimuth2 Calc_TrueAzimuth2;

//计算目标点相对于基础方向的相对方位
typedef void (*pCalc_RelAzimuth)(double abs_angel, double base_angel, double* rel_angel) ;
extern pCalc_RelAzimuth Calc_RelAzimuth;

//计算两点之间的距离
typedef void (*pCalc_Distance3)(const PointThreeDime_T p1,	const PointThreeDime_T p2, double* dis) ;
extern pCalc_Distance3 Calc_Distance3;

typedef void (*pCalc_Distance2)(const PointTwoDime_T p1,	const PointTwoDime_T p2, double* dis);
extern pCalc_Distance2 Calc_Distance2;

//计算目标点是否在从基点发出的锥体形波束的覆盖范围内
typedef void (*pCalc_IsBeamCover)(const JamBeamPara_T jam, const PointThreeDime_T base, const PointThreeDime_T target, bool* cover);
extern pCalc_IsBeamCover Calc_IsBeamCover;

//计算两点之间的通视距离
typedef void (*pCalc_GeoVisionDis)(double h1, double h2, double* dis);
extern pCalc_GeoVisionDis Calc_GeoVisionDis;

//计算目标点相对于基点的俯仰角【-90， 90】
typedef void (*pCalc_TargetElevation3)(const PointThreeDime_T target, const PointThreeDime_T base, double* ang) ;
extern pCalc_TargetElevation3 Calc_TargetElevation3;

typedef void (*pCalc_TargetElevation)(double targetZ, double baseZ, double distance, double* ang);
extern pCalc_TargetElevation Calc_TargetElevation;

//计算目标点相对于基点的相对航向
typedef void (*pCalc_TargetRelCourse)(const SpeedTwoDime_T tar, const SpeedTwoDime_T base, double* course);
extern pCalc_TargetRelCourse Calc_TargetRelCourse;

//计算目标点相对于基点的相对航速
typedef void (*pCalc_TargetRelSpeed)(const SpeedThreeDime_T tar,  const SpeedThreeDime_T base,	double* speed);
extern pCalc_TargetRelSpeed Calc_TargetRelSpeed;

//分贝毫瓦到瓦特的转换
typedef double (*pCalc_DbmWToWatt)(double DbmW);
extern pCalc_DbmWToWatt Calc_DbmWToWatt;

//瓦特到分贝毫瓦的转换
typedef double (*pCalc_WattToDbmW)(double Watt);
extern pCalc_WattToDbmW Calc_WattToDbmW;

//大气传输衰减计算
//频率Wave_Fre(MHz),距离Dis_Trans(m)
typedef void (*pCalc_WaveTransLoss)(double Wave_Fre, double Dis_Trans, double* loss);
extern pCalc_WaveTransLoss Calc_WaveTransLoss;

//定义 自动生成类型
class $ctx["so_folder"];

class $clsname
{
public:
    $clsname ( $ctx['so_folder'] *);
    ~$clsname (void);

    /**
    *@brief 组件初始化
    *@ 初始化性能参数集
    */
    bool init();
    /**
    *@brief 组件输入接口
    *@param paramSet 组件输入接口数据属性集
    */
    void input(const CParameterSet* paramSet);

    /**
    *@brief 组件输出接口
    *@param paramSet 组件输出接口数据属性集
    */
    void output(CParameterSet* paramSet);

    /**
    *@brief 组件接收事件接口
    *@param paramSet 组件接收事件数据属性集
    */
    void receiveEvent(const CEventParameterSet* paramSet);

    /**
    *@brief 组件发送事件接口
    *@param paramSet 组件发送事件数据属性集
    *@param sendIndex 当前发送的次数(从0开始的数字)
    */
    void sendEvent(CEventParameterSet* paramSet, uint32 sendIndex);

    /**
    *@brief 组件运行接口
    *@param simTime 组件运行仿真时间
    *@param dt 组件运行仿真步长
    *@return 组件运行状态码
    */
    LONGRESULT run(CEE_Time_t simTime, CEE_Time_t dt);



private:
    /**************************** 接口类指针 ****************************/

    $ctx["so_folder"] *pobj;

    /**************************** 性能参数列表 ****************************/

$for item in ctx['perf_def']:
    $ item_tp = '::'.join((item.it_ns, item.it_type))
        /* name:$item.it_cname
         * desc:$item.it_desc
         */
        $RefineContext(item_tp) m_$item.it_name;

$#
    /**************************** 发送Info列表 ****************************/

$for item in ctx['info_def']:
    $ item_tp = 'std::vector<' + '::'.join((item.cd_ns, item.cd_type)) + '>'
    $if item.cd_io == u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
            $RefineContext(item_tp) m_output_$item.cd_name;

$#
    /**************************** 接收Info列表 **************************/

$for item in ctx['info_def']:
    $ item_tp = 'std::vector<' + '::'.join((item.cd_ns, item.cd_type)) + '>'
    $if item.cd_io != u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
             $RefineContext(item_tp) m_input_$item.cd_name;

$#
    /**************************** 发送Event列表 ****************************/

$for item in ctx['evts_def']:
    $ item_tp = 'std::vector<' + '::'.join((item.cd_ns, item.cd_type)) + '>'
    $if item.cd_io == u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
            $RefineContext(item_tp) m_send_$item.cd_name;

$#

    /**************************** 接收Event列表 ****************************/

$for item in ctx['evts_def']:
    $ item_tp = 'std::vector<' + '::'.join((item.cd_ns, item.cd_type)) + '>'
    $if item.cd_io != u'输出':
            /** name: $item.cd_cname
             *  desc: $item.cd_desc
            */
            $RefineContext(item_tp) m_receive_$item.cd_name;

$#



};


#endif // $ctx['PJ_NAME']_IMPL_HPP_TMPL_H
