#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <vector>
#include <string>
#include <map>


#include "dialognamespace.h"
#include "outputwindow.h"
#include "embedpython.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_actionNameSpace_triggered();

    void on_listWidget_doubleClicked(const QModelIndex &index);

    void on_pushButton_3_clicked();

    //Internal use
    //show model data struct xml file
    void editModelDataStruct(const QString& name);
    void on_actionReloadmodel_triggered();

    //Timer Interval to check output message
    void onCheckOutputMessage();
signals:
    void modelNameChanged(const QString&);
    void modelExcelModelChanged(const QStringList&);
    void modelDataStructListChanged(const QStringList&);
    void outputMessage(const QStringList&);
private:
    Ui::MainWindow *ui;
    std::vector<std::pair<std::string, std::string> > nslist;
    OutputWindow* outdock;
    QString title;
    EmbedPython *ep;
};

#endif // MAINWINDOW_H
