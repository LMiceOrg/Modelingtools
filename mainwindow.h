#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <vector>
#include <string>
#include <map>
#include <QListWidgetItem>
#include <QKeyEvent>

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
    void editModelCodeFile(const QString& name);

    /// 生成动态菜单项
    void menuInit();
    /// 触发菜单
    void fileEdit(QAction*act);
    void recursiveAddMenu(QMenu*, QActionGroup*, const QString& path, const QString& folder);

    void on_actionReloadmodel_triggered();

    //Timer Interval to check output message
    void onCheckOutputMessage(const QString& emsg);
    void onInformationMessage(const QString& emsg);
    void on_pushButton_4_clicked();

    void on_actionQuit_Modeltools_triggered();

    void on_pushButton_5_clicked();

    void on_actionDumpProject_triggered();

    void on_actionRestoreProject_triggered();

    void on_pushButton_6_clicked();

    void on_listWidget_itemChanged(QListWidgetItem *item);

    //Keypress
    void on_KeyPressed(int type);

    void on_actionEnlarge_triggered();

    void on_actionBesmall_triggered();

    void on_actionClearProject_triggered();

    void on_modelParam_Buttopn_clicked();

    void on_pushButton_7_clicked();

    void on_actionSelectModel_triggered();

    void on_actionCreateCode_triggered();

    void on_actionModelParam_triggered();

    void ReadExcelList(const QString& folder);

signals:
    void modelNameChanged(const QString&);
    void modelExcelModelChanged(const QStringList&);
    void modelExcelModelAdd(const QString&);
    void modelExcelModelRemove(const QString&);
    void modelDataStructListChanged(const QStringList&);
    void modelModelDescListChanged(const QStringList&);
    void outputMessage(const QStringList&);
    void outputInformation(const QString&);
    void modelCodeFileListChanged(const QStringList&);
private:
    Ui::MainWindow *ui;
//    std::vector<std::pair<std::string, std::string> > nslist;
    OutputWindow* outdock;
    QString title;
    EmbedPython *ep;
    QsciLexerXML* xmlparser;
    QsciLexerCPP* cppparser;
    bool isLoading;
};

#endif // MAINWINDOW_H
