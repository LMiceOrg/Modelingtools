#include "stdafx.h"
#include "mainwindow.h"

//TODO: [张高峰]增加错误提示功能


int main(int argc, char *argv[])
{
    qDebug()<<sizeof(wchar_t);
    //qDebug()<<Py_GetPath();
    QApplication a(argc, argv);
    //qDebug()<<"begin sys set"<<argc<<argv[0];
    //Py_InspectFlag = 1;
    //Py_Main(argc, argv);
    //PySys_SetArgvEx(argc, argv, 0);
    int ret;
    {
        MainWindow w;
        w.show();
        ret = a.exec();
    }

    return ret;
}
