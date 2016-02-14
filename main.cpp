#include "stdafx.h"
#include "mainwindow.h"

#include <QTranslator>
#include <stdint.h>

#if defined(__APPLE__)
#include <mach-o/dyld.h>

//#include "../build-qautotools-Desktop_Qt_5_3_clang_64bit-Release/modelingtools.app/Contents/MacOS/common/include/NTSim.h"
//NTSim_Jam::JamBeamPara_T o;
//NTSim_Global::PlatDAdjConPara_T o2;


#elif defined(WIN32)
#include <AppSimKernel.h>

//#include "../../common/include/NTSim.h"
#endif


int main(int argc, char *argv[])
{

//    //IEEE754
//    double dbl = 1;
//    if(isnan(dbl)) {
//        qDebug()<<"wu xiao";
//    }
//    dbl += 1000;
//    qDebug()<<dbl;

//    //header
//    NTSim::Info_IRReconTar_T obj, obj3;

//    qDebug()<<"obj size="<<obj.size();
//    qDebug()<<"obj onsize="<<obj.OnSize();

//    //init
//    obj.clear();

//    //run
//    NTSim::IRReconTarPara_T o1;
//    for(int i=0; i<5; ++i) {
//        o1.TarGNum = 111 + i;
//        obj.IRReconTarPara.push_back(o1);
//    }
//    qDebug()<<"01 size="<<o1.size();
//    obj.IRReconTarNum = 5;
//    wsprintf(obj.Info_Basic.ID.value, _T("12111") );

    //output
//    {
//        int sz = obj.size();
//        char* buff;
//        buff = new char[sz];
//        obj.pack(buff, sz);
//        std::string str;
//        str.insert(str.begin(), buff, buff+sz);
//        delete[] buff;
//    }

//    int sz = obj.size();
//    qDebug()<<"size="<<sz;
//    std::vector<char> vec;
//    vec.resize(sz);
//    sz = obj.pack(&vec[0], sz);
//    std::string str;
//    str.clear();
//    str.insert(str.begin(), vec.begin(), vec.end());



//    //receive, input
//    obj3.clear();
//    qDebug()<<"IRReconTarNum="<<obj3.IRReconTarNum;
//    obj3.unpack(str.c_str(), str.size());
//    qDebug()<<"IRReconTarNum="<<obj3.IRReconTarNum;
//    qDebug()<<"Para_WorkState=";
//    wprintf(_T("%s\n"), AppSim::toTString(obj3.Info_Basic.ID).c_str());

//    qDebug()<<"IRReconTarPara size="<<obj3.IRReconTarPara.size();

//    NTSim::IRReconTarPara_T &o3 = obj3.IRReconTarPara[2];
//    qDebug()<<"TarGNum="<<o3.TarGNum;

    //qDebug()<<o.size();
//    printf("size %d\n", o.size());
//    o.clear();
//    o.data();
//    //qDebug()<<o2.size();
//    printf("size %d\n", o2.size());
//    o2.clear();
    //qDebug()<<o2.size();

//    qDebug()<<o.is_pod()<<o.size();
//    o.init();
//#ifdef __APPLE__
//   uint32_t sz = _dyld_image_count();
//   qDebug()<<"All Shared libraries:"<<sz;
//   for(size_t i=0; i<sz; ++i){
//       qDebug()<<_dyld_get_image_name(i);
//   }
//#endif

    //qDebug()<<"begin sys set"<<argc<<argv[0];
    //Py_InspectFlag = 1;
    //Py_Main(argc, argv);
    //PySys_SetArgvEx(argc, argv, 0);
    QApplication a(argc, argv);
    /** View-style */
    {
        QFile file(":/css/lightstyle.css");
        if( file.open(QIODevice::ReadOnly | QIODevice::Text) ) {
            QString style(file.readAll());
            file.close();
            a.setStyleSheet(style);
        }
    }
    /** Translation */
    QTranslator tran;
    tran.load(a.applicationDirPath() + "/modelingtools.zh_CN");
    a.installTranslator(&tran);

    int ret;
    {
        MainWindow w;
        w.show();
        ret = a.exec();
    }

    return ret;
}

//#if __has_feature(is_pod)
//#warning is_pod
//#endif

//#if (__GNUC__ > 4)
//#warning gnuc > 4
//#endif

//#if (__GNUC__ == 4 && __GNUC_MINOR__ >= 3)
//#warning gnuc 4.3
//#endif
