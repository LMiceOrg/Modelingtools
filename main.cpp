#include "stdafx.h"
#include "mainwindow.h"

//TODO: [张高峰]增加错误提示功能


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    int ret;
    {
        MainWindow w;
        w.show();
        ret = a.exec();
    }

    return ret;
}
