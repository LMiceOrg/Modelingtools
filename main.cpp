#include "stdafx.h"
#include "mainwindow.h"


#if defined(__APPLE__)
#include <mach-o/dyld.h>
#elif WIN32

#endif

#include "../build-qautotools-Desktop_Qt_5_3_clang_64bit-Release/modelingtools.app/Contents/MacOS/NTSim.h"
//NTSim_Jam::JamBeamPara_T o;

int main(int argc, char *argv[])
{
//    o.data();


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
