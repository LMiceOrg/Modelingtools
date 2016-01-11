#include "stdafx.h"
#include "mainwindow.h"

//TODO: 增加错误提示功能

#if defined(__APPLE__)
#include <mach-o/dyld.h>
#elif WIN32

#endif

int main(int argc, char *argv[])
{
    //qDebug()<<sizeof(wchar_t);
    //qDebug()<<Py_GetPath();
    QApplication a(argc, argv);
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
