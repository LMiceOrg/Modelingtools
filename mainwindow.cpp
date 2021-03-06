#include "stdafx.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QDebug>
#include <QFormLayout>
#include <QLabel>

#include <string.h>
#include <QMultiMap>
#include <QTimer>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    menuInit();

    xmlparser = new QsciLexerXML(this);
    cppparser = new QsciLexerCPP(this);



    outdock=new OutputWindow(this);
    connect(this, SIGNAL(modelNameChanged(QString)),
            outdock, SLOT(modelNameChanged(QString)) );

    connect(this, SIGNAL(modelExcelModelChanged(QStringList)),
            outdock, SLOT(modelExcelListChanged(QStringList)) );

    connect(this, SIGNAL(modelExcelModelAdd(QString)),
            outdock, SLOT(modelExcelAddFile(QString)) );

    connect(this, SIGNAL(modelExcelModelRemove(QString)),
            outdock, SLOT(modelExcelRemoveFile(QString)) );

    connect(this, SIGNAL(modelDataStructListChanged(QStringList)),
            outdock, SLOT(modelDataStructFiles(QStringList)) );
    connect(this, SIGNAL(modelModelDescListChanged(QStringList)),
            outdock, SLOT(modelModelDscFiles(QStringList)) );

    connect(outdock, SIGNAL(currentDataStructChanged(QString)),
            this, SLOT(editModelDataStruct(QString)) );

    connect(this, SIGNAL(modelCodeFileListChanged(QStringList)),
            outdock, SLOT(modelModelCodeFiles(QStringList)) );
    connect(outdock, SIGNAL(currentCodeFileChanged(QString)),
            this, SLOT(editModelCodeFile(QString)) );


    addDockWidget(Qt::LeftDockWidgetArea, outdock);


    title = windowTitle();

#if __APPLE__
    //Debug purpose
    ui->lineEdit->setText("/Users/hehao/work/doc/modelingtools/res20160109/model");
#elif _WIN32
    //ui->lineEdit->setText("i:/dist3/20151229/model");
    ui->lineEdit->setText("E:/model");
#endif

    ep = new EmbedPython(this);

    //修改默认路径
    updateModelFolder();


    connect(ep, SIGNAL(errorTrigger(QString)), this, SLOT(onCheckOutputMessage(QString)) );

    connect(this, SIGNAL(outputInformation(QString)),
            this, SLOT(onInformationMessage(QString)));

    ui->tabWidget->setTabText(0, tr("Output Window"));

    QPixmap px(":/flatastic2");
    int px_width = 112, px_height = 112;
    ui->actionNameSpace->setIcon(QIcon(px.copy(     0*px_width,2*px_height,     px_width,px_height)));
    ui->actionReloadmodel->setIcon(QIcon(px.copy(   4*px_width,5*px_height,     px_width,px_height)));
    ui->actionDumpProject->setIcon(QIcon(px.copy(   3*px_width,0*px_height,     px_width,px_height)));
    ui->actionRestoreProject->setIcon(QIcon(px.copy(3*px_width,4*px_height,     px_width,px_height)));
    ui->actionClearProject->setIcon(QIcon(px.copy(  1*px_width,1*px_height,     px_width,px_height)));
    ui->actionSelectModel->setIcon(QIcon(px.copy(   0*px_width,4*px_height,     px_width,px_height)));
    ui->actionCreateCode->setIcon(QIcon(px.copy(    2*px_width,4*px_height,     px_width,px_height)));
    ui->actionModelParam->setIcon(QIcon(px.copy(    2*px_width,5*px_height,     px_width,px_height)));
    ui->mainToolBar->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
    ui->mainToolBar->setIconSize(QSize(16,16));

    //隐藏按钮
    ui->pushButton_7->setVisible(false);
    ui->modelParam_Buttopn->setVisible(false);



    showMaximized();

}

MainWindow::~MainWindow()
{
//    delete ep;

    delete ui;
}

// Choose model folder
void MainWindow::on_pushButton_clicked()
{
    QString folder = QFileDialog::getExistingDirectory(
                this,
                tr("Open Model Directory"),
                ui->lineEdit->text(),
                QFileDialog::ShowDirsOnly
                | QFileDialog::DontResolveSymlinks);

    if(folder.isEmpty()) {
        return;
    }

    ui->lineEdit->setText(folder);
    ReadExcelList(folder);
}
void MainWindow::ReadExcelList(const QString& folder)
{
    QDir dir(folder);
    if( !dir.exists() ||
            dir.dirName().compare(tr("model"), Qt::CaseInsensitive) != 0) {
        //Dir is not a valid model folder
        QMessageBox::critical(
                    this,
                    title,
                    tr("Dir<span style=\"color:#ee0e0e;font-weight:bold\">[%1]</span>"
                       " is not a valid model folder.<p>Tips: Dir should be <b>[.../%2]</b></p>")
                    .arg(folder)
                    .arg(tr("model")));

        return;
    }
    setWindowTitle( tr("%1 - [Opening Model] %2").arg(title).arg(folder) );
    emit modelNameChanged(folder);
    emit outputInformation(tr("Parsing: %1").arg(folder));
    isLoading = true;

    ep->callModel("GetFileList", "s", folder.toUtf8().data());
//    qDebug()<<"call GetFileList"<<ep->returnType();
//    qDebug()<<"test "<<folder;
    if( ep->returnType() && strcmp(ep->returnType(), "list") == 0) {
        PyObject* ret = ep->returnObject();
        //qDebug()<<"ret="<<ret;
        for(Py_ssize_t i=0; i<PyList_Size(ret); ++i) {
            PyObject* o = PyList_GetItem(ret, i);
            if(o && PyString_Check(o)) {
                QString text(PyString_AS_STRING(o));
                //qDebug()<<"item["<<i<<"]="<<text;
                if(ui->listWidget->findItems(text, 0).size() == 0) {
                    QListWidgetItem *item = new QListWidgetItem(ui->listWidget);
                    item->setText( QString(PyString_AsString(o)) );
                }
            }
        }
    }

    isLoading = false;
    emit outputInformation(tr("Parse... Done"));

}

void MainWindow::updateModelFolder()
{
    //修改默认路径
    {
        ep->callModel("GetModelFolder");
        //qDebug()<<"call";
        PyObject* o = ep->returnObject();
        //qDebug()<<"call0";
        if( o && PyString_Check(o)) {
            //qDebug()<<"call1";
            QString s = QString( PyString_AsString(o) );
            ui->lineEdit->setText(s);
        }
        //qDebug()<<"call2";
    }
    onCheckOutputMessage(ep->errorMessage());
}

//Validate Excel files
void MainWindow::on_pushButton_2_clicked()
{

    QStringList xlModels;
    QListWidgetItem * item;
    QFont font;
    emit outputInformation(tr("Checking Excel"));
    for(int i=0; i < ui->listWidget->count(); ++i) {
        item = ui->listWidget->item(i);

        if(item) {
            ep->callModel("CheckExcelFileModel", "s", item->text().toUtf8().data());
            //qDebug()<<item->text()<<" valid:" <<ep->returnType();
            if(strcmp(ep->returnType(), "NoneType") == 0) {
                item->setIcon(style()->standardIcon(QStyle::SP_TrashIcon));
                font = item->font();
                font.setUnderline(true);
                font.setItalic(true);
                item->setFont(font);
                item->setCheckState(Qt::Unchecked);
                item->setData(Qt::UserRole, false);
            } else {
                item->setIcon(style()->standardIcon(QStyle::SP_ComputerIcon));
                font = item->font();
                font.setBold(true);
                item->setFont(font);
                item->setCheckState(Qt::Checked);
                item->setData(Qt::UserRole, true);

//                QStringList sl;
//                PyObject* ret = ep->returnObject();
//                for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
//                    sl.push_back( PyString_AsString(PyList_GetItem(ret, i)) );
//                }
//                item->setData(Qt::UserRole+1, sl);
//                qDebug()<<sl;
                xlModels.push_back(item->text());
            }
//            QDir dir(item->text());
//            QString p = QString("datafile = cp.parseFile('%1')\n").arg( dir.absolutePath());
//            qDebug()<<"parse command:"<<p;
//            PyRun_SimpleString(p.toStdString().c_str());
//            PyObject* module = PyImport_ImportModule("__main__");
//            PyObject* datafile = PyObject_GetAttrString(module, "datafile");
//            if(PyString_Check(datafile)) {
//                QString text(PyString_AsString(datafile));
//                qDebug()<<"xml file is :"<<text;
//                //ui->textBrowser->setSource(QUrl::fromLocalFile(text));
//                QFile f(text);
//                if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
//                    return;
//                QString ctx = QString(f.readAll());
//                ui->textEdit->setUtf8(true);
//                ui->textEdit->setText(ctx);
//                ui->textEdit->setAutoIndent(true);

//                ui->tabWidget->setTabText(0, tr("data struct gen detail"));
//                foreach(QObject* child, ui->tabWidget->widget(0)->children() ) {
//                    child->deleteLater();
//                }

//                QFormLayout *flayout = new QFormLayout(ui->tabWidget->widget(0));
//                QLabel* label = new QLabel();
//                label->setWordWrap(true);
//                label->setText(QString(tr("<p style=\"color='#ee00cc'\">Generate Data XML from %1</p>").arg(text)));
//                label->setTextFormat(Qt::RichText);
//                flayout->addWidget(label);
//            }
//            Py_XDECREF(datafile);
//            Py_XDECREF(module);
        }
    }

    emit modelExcelModelChanged(xlModels);
    emit outputInformation(tr("Check... Done"));
}

void MainWindow::on_actionNameSpace_triggered()
{
    ui->actionNameSpace->menu()->popup(QCursor::pos());
}

void MainWindow::on_listWidget_itemChanged(QListWidgetItem *item)
{
    if(isLoading)
        return;

//    disconnect(ui->listWidget, SIGNAL(itemChanged(QListWidgetItem*))
//               ,this, SLOT(on_listWidget_itemChanged(QListWidgetItem*)) );

//    isLoading = true;
//    qDebug()<<item;
    if(item) {
        if(item->flags().testFlag(Qt::ItemIsUserCheckable)) {
            Qt::CheckState cs = item->checkState();
            if(cs == Qt::Checked) {
//                cs = Qt::Unchecked;
//                qDebug()<<"list change";
                //item->setCheckState(cs);
                emit modelExcelModelAdd(item->text());

            }else if(cs == Qt::Unchecked && item->data(Qt::UserRole).toBool() == true) {
//                cs = Qt::Checked;
                //item->setCheckState(cs);
                emit modelExcelModelRemove(item->text());
            }
        }
    }

//    connect(ui->listWidget, SIGNAL(itemChanged(QListWidgetItem*))
//               ,this, SLOT(on_listWidget_itemChanged(QListWidgetItem*)) );

    //    isLoading = false;
}

void MainWindow::on_KeyPressed(int type)
{
    QFont fnt = ui->textEdit->lexer()->defaultFont();
    if(type == 1) {
        int sz = fnt.pointSize() + 2;
        //if(sz >32) sz = 32;
        fnt.setPointSize( sz );
    } else {
        int sz = fnt.pointSize() - 2;
        if(sz < 8) sz = 8;
        fnt.setPointSize( sz );

    }
    ui->textEdit->lexer()->setFont(fnt);
}

void MainWindow::on_listWidget_doubleClicked(const QModelIndex &index)
{
    QListWidgetItem * item;
    item = ui->listWidget->item(index.row());
    if(item) {
        if(item->flags().testFlag(Qt::ItemIsUserCheckable)) {
            Qt::CheckState cs = item->checkState();
            if(cs == Qt::Unchecked)
                cs = Qt::Checked;
            else
                cs = Qt::Unchecked;
            item->setCheckState(cs);
        }
    }

}

//生成数据定义XML
void MainWindow::on_pushButton_3_clicked()
{
    emit outputInformation(tr("Generating datastruct"));
    ep->callModel("SaveDataStruct", NULL);
    QStringList dsfiles;
    PyObject* ret = ep->returnObject();
    if(ret && PyList_Check(ret)) {
        for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
            dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i))                              );
        }
        emit modelDataStructListChanged(dsfiles);
    }
    emit outputInformation(tr("Generating datastruct... Done"));

}

void MainWindow::editModelDataStruct(const QString &name)
{
    QFile f(name);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
        return;
    QString ctx = QString(f.readAll());
    f.close();
    ui->textEdit->setUtf8(true);
    ui->textEdit->setText(ctx);
    ui->textEdit->setAutoIndent(true);

    ui->textEdit->setLexer(xmlparser);
    ui->textEdit->setFolding(QsciScintilla::BoxedTreeFoldStyle);
    // Show line number in left side
    ui->textEdit->setMarginLineNumbers(QsciScintilla::SC_MARGIN_NUMBER, true);
    ui->textEdit->setMarginWidth(QsciScintilla::SC_MARGIN_NUMBER, 32);
    // Adjust font style
    QFont fnt =xmlparser->font(QsciLexerXML::Tag);
    fnt.setPointSize(14);
//    fnt.setBold(true);
    //ui->textEdit->setFont(fnt);
    xmlparser->setFont(fnt, QsciLexerXML::Tag);
    fnt =xmlparser->font(QsciLexerXML::HTMLDoubleQuotedString);
    fnt.setPointSize(16);
    fnt.setItalic(true);
    //ui->textEdit->setFont(fnt);
    xmlparser->setFont(fnt, QsciLexerXML::HTMLDoubleQuotedString);
}

//编辑代码文件
void MainWindow::editModelCodeFile(const QString &name)
{
    QFile f(name);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
        return;
    QString ctx = QString(f.readAll());
    f.close();
    ui->textEdit->setUtf8(true);
    ui->textEdit->setText(ctx);
    ui->textEdit->setAutoIndent(true);

    ui->textEdit->setLexer(cppparser);
    ui->textEdit->setFolding(QsciScintilla::BoxedTreeFoldStyle);
    // Show line number in left side
    ui->textEdit->setMarginLineNumbers(QsciScintilla::SC_MARGIN_NUMBER, true);
    ui->textEdit->setMarginWidth(QsciScintilla::SC_MARGIN_NUMBER, 32);
    // Adjust font style
//    QFont fnt =xml->font(QsciLexerXML::Tag);
//    fnt.setPointSize(14);
////    fnt.setBold(true);
//    //ui->textEdit->setFont(fnt);
//    xml->setFont(fnt, QsciLexerXML::Tag);
//    fnt =xml->font(QsciLexerXML::HTMLDoubleQuotedString);
//    fnt.setPointSize(16);
//    fnt.setItalic(true);
//    //ui->textEdit->setFont(fnt);
    //    xml->setFont(fnt, QsciLexerXML::HTMLDoubleQuotedString);
}

void MainWindow::menuInit()
{
    QStringList sl;
    QStringList filters;
    filters << "*.cpp" << "*.cxx" << "*.cc"<<"*.hpp"
            <<"*.h"<<"*.c"
           <<"*.py"<<"*.xml"
          <<"*.ini";
    QActionGroup *grp = new QActionGroup(this);
    connect(grp, SIGNAL(triggered(QAction*)), this, SLOT(fileEdit(QAction*)));
    QAction* act = ui->actionNameSpace;
    QMenu* menu = act->menu();
    if(!menu) {
        act->setMenu(new QMenu("Python code"));
        menu = act->menu();
    }
#if _WIN32
    QDir dir(qApp->applicationDirPath());
    dir.cd("Lib");
    dir.cd("site-packages");
    dir.cd("autotools");
#elif __APPLE__
    QDir dir(qApp->applicationDirPath());
    dir.cdUp();
    dir.cd("Resources");
    dir.cd("site-packages");
    dir.cd("autotools");
#endif
    // folder
    sl = dir.entryList(QDir::AllDirs|QDir::NoDotAndDotDot);
    for(int i=0; i< sl.size(); ++i) {
        QMenu *m = menu->addMenu(sl.at(i));
        recursiveAddMenu(m, grp, dir.absolutePath(), sl.at(i));
    }
    sl = dir.entryList(filters, QDir::Files);
    for(int i=0; i< sl.size(); ++i) {
        QString file = dir.absolutePath() + QDir::separator() + sl.at(i);
        act = new QAction(sl.at(i), grp);
        act->setData( file );
        //connect(act, SIGNAL(triggered()), this, SLOT(on_actionNameSpace123_triggered()) );

        menu->addAction(act);
        //m->setActiveAction(act);
    }
}

void MainWindow::fileEdit(QAction * act)
{
    QString cfgfile = act->data().toString();
    if(! cfgfile.isEmpty()) {
#if __APPLE__
//    QDir dir(qApp->applicationDirPath());
//    dir.cdUp();
//    dir.cd("Resources");
//    dir.cd("autotools");
//    QString cfgfile = dir.filePath("__init__.py");

    DialogNamespace dlg(cfgfile, ep);
    dlg.exec();
#elif _WIN32
//    QDir dir(qApp->applicationDirPath());
//    //dir.cdUp();
//    dir.cd("Lib");
//    dir.cd("site-packages");
//    dir.cd("autotools");
//    QString cfgfile = dir.filePath("__init__.py");

    DialogNamespace dlg(cfgfile, ep);
    dlg.exec();

#endif
    if(cfgfile.endsWith(tr("autotools%1__init__.py")
                        .arg(QDir::separator())
                        )) {
        updateModelFolder();
    }
    }
}

void MainWindow::recursiveAddMenu(QMenu * menu, QActionGroup * grp, const QString &path, const QString &folder)
{
    QAction* act;
    QStringList sl;
    QStringList filters;
    filters << "*.cpp" << "*.cxx" << "*.cc"<<"*.hpp"
            <<"*.h"<<"*.c"
           <<"*.py"<<"*.xml"
          <<"*.ini";

    QDir dir(path);
    dir.cd(folder);

    // folder
    sl = dir.entryList(QDir::AllDirs|QDir::NoDotAndDotDot);
    for(int i=0; i< sl.size(); ++i) {
        QMenu *m = menu->addMenu(sl.at(i));
        recursiveAddMenu(m, grp, dir.absolutePath(), sl.at(i));
    }
    sl = dir.entryList(filters, QDir::Files);
    for(int i=0; i< sl.size(); ++i) {
        QString file = dir.absolutePath() + QDir::separator() + sl.at(i);
        act = new QAction(sl.at(i), grp);
        act->setData( file );
        //connect(act, SIGNAL(triggered()), this, SLOT(on_actionNameSpace123_triggered()) );

        menu->addAction(act);
        //m->setActiveAction(act);
    }

}

void MainWindow::on_actionReloadmodel_triggered()
{
    ep->reload();
}

void MainWindow::onCheckOutputMessage(const QString &emsg)
{

    if (!emsg.isEmpty()) {
        QStringList sl = emsg.split("\n");
        if (sl.size() > 0) {
            emit outputMessage(sl);
            ui->errListWidget->addItem(
                        new QListWidgetItem(style()->standardIcon(QStyle::SP_MessageBoxCritical),
                                            sl.at(0),
                                            ui->errListWidget));

            ui->errListWidget->addItems(sl);
        }
    }

}

void MainWindow::onInformationMessage(const QString &emsg)
{
    if (!emsg.isEmpty()) {
        QStringList sl = emsg.split("\n");
        if (sl.size() > 0) {
            emit outputMessage(sl);
            ui->errListWidget->addItem(
                        new QListWidgetItem(style()->standardIcon(QStyle::SP_MessageBoxInformation),
                                            sl.at(0),
                                            ui->errListWidget));
            sl.pop_front();
            if (sl.size() > 0) {
                ui->errListWidget->addItems(sl);
            }
        }
    }
}

// Generate Dsc File
void MainWindow::on_pushButton_4_clicked()
{
    emit outputInformation(tr("Generating model desc..."));
    ep->callModel("SaveModelDesc");
    QStringList dsfiles;
    PyObject* ret = ep->returnObject();
    if(ret && PyList_Check(ret)) {
        for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
            dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i)) );
        }
        emit modelModelDescListChanged(dsfiles);
    }
    emit outputInformation(tr("Generating model desc... Done"));
}

void MainWindow::on_actionQuit_Modeltools_triggered()
{
    qApp->quit();
}

// 生成模型代码
void MainWindow::on_pushButton_5_clicked()
{
    QStringList dsfiles;
    emit outputInformation(tr("Generating model code..."));
    ep->callModel("SaveCppProject", NULL);
    PyObject* ret = ep->returnObject();
    if(ret && PyList_Check(ret)) {
        for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
            dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i)) );
        }
        emit modelCodeFileListChanged(dsfiles);
    } else if(ret && PyString_Check(ret)) {
        QString files = PyString_AsString(ret);
        dsfiles = files.split(",");
        //qDebug()<<files;
        emit modelCodeFileListChanged(dsfiles);
    }
    emit outputInformation(tr("Generating model code... Done"));
}

void MainWindow::on_actionDumpProject_triggered()
{
    ep->callModel("Backup", "s", "proj.bak");
}

//载入工程
void MainWindow::on_actionRestoreProject_triggered()
{
    PyObject* ret;
    ep->callModel("Restore", "s", "proj.bak");

    //获取工程路径
    ep->callModel("GetModelProjectName");
    QString proj_root;
    ret = ep->returnObject();
    if(ret && PyString_Check(ret)) {
        proj_root = PyString_AsString(ret);
        setWindowTitle( tr("%1 - [Opening Model] %2").arg(title).arg(proj_root) );
        emit modelNameChanged(proj_root);
    }

    //获取模型的源列表
    ep->callModel("GetSourceList");
    QStringList dsfiles;
    ret = ep->returnObject();
    if(!ret || !PyList_Check(ret)) {
        //return type is not a list
        return;
    }

    isLoading = true;

    QListWidgetItem * item;
    QFont font;
    ui->listWidget->clear();
    for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
        QString xlfile = PyString_AsString(PyList_GetItem(ret, i));
        dsfiles.push_back( xlfile  );

        item = new QListWidgetItem(ui->listWidget);
        item->setText( xlfile );
        item->setIcon(style()->standardIcon(QStyle::SP_ComputerIcon));
        font = item->font();
        font.setBold(true);
        item->setFont(font);
        item->setCheckState(Qt::Checked);
        item->setData(Qt::UserRole, true);
    }
//    qDebug()<<dsfiles;
    emit modelExcelModelChanged(dsfiles);

    isLoading = false;
}

// Parse Excel Files
void MainWindow::on_pushButton_6_clicked()
{
//    QMultiMap<QString, QStringList> mp;
    QListWidgetItem * item;
    QString param2;

    emit outputInformation(tr("Parsing Excel files..."));
    for(int i=0; i < ui->listWidget->count(); ++i) {
        item = ui->listWidget->item(i);
        if(item->checkState() == Qt::Checked) {
//            QStringList sl = item->data(Qt::UserRole+1).toStringList();
//            sl.push_back(item->text());
//            mp.insert(sl[0], sl);
            param2.append(item->text()).append(",");


        }
    }
    ep->callModel("ParseSources", "s", param2.toUtf8().data());

    emit outputInformation(tr("Parsing Excel files... Done"));

//    QList<QString> keys = mp.uniqueKeys();
//    for(int k=0; k< keys.size(); ++k) {
//        QString key = keys.at(k);

//        QList<QStringList> slist = mp.values(key);
//        QString param2;
//        for(int j=0; j< slist.size(); ++j) {
//            param2.append( slist.at(j).value(4) )
//                    .append(",");
//        }
////        qDebug()<<"call GenerateDataStruct:"<<param2;
//        //ep->callModel("GenerateDataStruct", "(ss)", key.toUtf8().data(), param2.toUtf8().data());
//        ep->callModel("ParseSources", "s", param2.toUtf8().data());

//        //qDebug()<<keys.size()<<slist.size()<<"Call GenerateDataStruct:"<<key;

//    }
}



void MainWindow::on_actionEnlarge_triggered()
{
    on_KeyPressed(1);
}

void MainWindow::on_actionBesmall_triggered()
{
    on_KeyPressed(0);
}

void MainWindow::on_actionClearProject_triggered()
{
    ep->callModel("ClearProject");
    ui->errListWidget->clear();
}

void MainWindow::on_modelParam_Buttopn_clicked()
{
    emit outputInformation(tr("Creating model params..."));
    ep->callModel("SaveModelParam");
    emit outputInformation(tr("Creating model params... Done"));
}

void MainWindow::on_pushButton_7_clicked()
{
    on_actionClearProject_triggered();
    on_pushButton_6_clicked();
    on_pushButton_3_clicked();
    on_pushButton_4_clicked();
    on_pushButton_5_clicked();

}

void MainWindow::on_actionSelectModel_triggered()
{
    ReadExcelList(ui->lineEdit->text());
    on_pushButton_2_clicked();
}

void MainWindow::on_actionCreateCode_triggered()
{
    on_pushButton_7_clicked();
}

void MainWindow::on_actionModelParam_triggered()
{
    on_modelParam_Buttopn_clicked();
}
