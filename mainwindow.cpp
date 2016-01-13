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

    QsciLexerXML *xml = new QsciLexerXML(this);
    ui->textEdit->setLexer(xml);
    ui->textEdit->setFolding(QsciScintilla::BoxedTreeFoldStyle);
    // Show line number in left side
    ui->textEdit->setMarginLineNumbers(QsciScintilla::SC_MARGIN_NUMBER, true);
    ui->textEdit->setMarginWidth(QsciScintilla::SC_MARGIN_NUMBER, 32);
    // Adjust font style
    QFont fnt =xml->font(QsciLexerXML::Tag);
    fnt.setPointSize(14);
//    fnt.setBold(true);
    //ui->textEdit->setFont(fnt);
    xml->setFont(fnt, QsciLexerXML::Tag);
    fnt =xml->font(QsciLexerXML::HTMLDoubleQuotedString);
    fnt.setPointSize(16);
    fnt.setItalic(true);
    //ui->textEdit->setFont(fnt);
    xml->setFont(fnt, QsciLexerXML::HTMLDoubleQuotedString);
    showMaximized();

    outdock=new OutputWindow(this);
    connect(this, SIGNAL(modelNameChanged(QString)), outdock, SLOT(modelNameChanged(QString)) );
    connect(this, SIGNAL(modelExcelModelChanged(QStringList)), outdock,
            SLOT(modelExcelListChanged(QStringList)) );
    connect(this, SIGNAL(modelDataStructListChanged(QStringList)),
            outdock, SLOT(modelDataStructFiles(QStringList)) );
    connect(this, SIGNAL(modelModelDescListChanged(QStringList)),
            outdock, SLOT(modelModelDscFiles(QStringList)) );

    connect(outdock, SIGNAL(currentDataStructChanged(QString)),
            this, SLOT(editModelDataStruct(QString)) );

    addDockWidget(Qt::LeftDockWidgetArea, outdock);


    title = windowTitle();

#if __APPLE__
    //Debug purpose
    ui->lineEdit->setText("/Users/hehao/work/doc/modelingtools/res20160109/model");
#endif

    ep = new EmbedPython(this);
    connect(ep, SIGNAL(errorTrigger(QString)), this, SLOT(onCheckOutputMessage(QString)) );

    onCheckOutputMessage(ep->errorMessage());

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

}

//Validate Excel files
void MainWindow::on_pushButton_2_clicked()
{

    QStringList xlModels;
    QListWidgetItem * item;
    QFont font;
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

                QStringList sl;
                PyObject* ret = ep->returnObject();
                for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
                    sl.push_back( PyString_AsString(PyList_GetItem(ret, i)) );
                }
                item->setData(Qt::UserRole+1, sl);
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
}

void MainWindow::on_actionNameSpace_triggered()
{
    nslist.push_back(std::pair<std::string, std::string>("Global", "NTSim_Global"));
    DialogNamespace dlg(nslist);
    dlg.exec();
}

void MainWindow::on_listWidget_doubleClicked(const QModelIndex &index)
{
    QListWidgetItem * item;
    item = ui->listWidget->item(index.row());
    if(item) {
        if(item->flags().testFlag(Qt::ItemIsUserCheckable)) {
            Qt::CheckState cs = item->checkState();
            if(cs == Qt::Checked) {
                cs = Qt::Unchecked;
                item->setCheckState(cs);
            }else if(cs == Qt::Unchecked && item->data(Qt::UserRole).toBool() == true) {
                cs = Qt::Checked;
                item->setCheckState(cs);
            }
        }
    }
}

//生成数据定义XML
void MainWindow::on_pushButton_3_clicked()
{

    ep->callModel("SaveDataStruct", NULL);
    QStringList dsfiles;
    PyObject* ret = ep->returnObject();
    if(ret && PyList_Check(ret)) {
        for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
            dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i))                              );
        }
        emit modelDataStructListChanged(dsfiles);
    }


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

// Generate Dsc File
void MainWindow::on_pushButton_4_clicked()
{
    ep->callModel("SaveModelDesc");
    QStringList dsfiles;
    PyObject* ret = ep->returnObject();
    if(ret && PyList_Check(ret)) {
        for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
            dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i)) );
        }
        emit modelModelDescListChanged(dsfiles);
    }
}

void MainWindow::on_actionQuit_Modeltools_triggered()
{
    qApp->quit();
}

void MainWindow::on_pushButton_5_clicked()
{
    ep->callModel("SaveCppProject", NULL);
}

void MainWindow::on_actionDumpProject_triggered()
{
    ep->callModel("Backup", "s", "proj.bak");
}

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
    for(Py_ssize_t i=0; i< PyList_Size(ret); ++i) {
        dsfiles.push_back( PyString_AsString(PyList_GetItem(ret, i))  );
    }
//    qDebug()<<dsfiles;
    emit modelExcelModelChanged(dsfiles);
}

// Parse Excel Files
void MainWindow::on_pushButton_6_clicked()
{
    QMultiMap<QString, QStringList> mp;
    QListWidgetItem * item;
    for(int i=0; i < ui->listWidget->count(); ++i) {
        item = ui->listWidget->item(i);
        if(item->checkState() == Qt::Checked) {
            QStringList sl = item->data(Qt::UserRole+1).toStringList();
            sl.push_back(item->text());
            mp.insert(sl[0], sl);

        }
    }


    QList<QString> keys = mp.uniqueKeys();
    for(int k=0; k< keys.size(); ++k) {
        QString key = keys.at(k);

        QList<QStringList> slist = mp.values(key);
        QString param2;
        for(int j=0; j< slist.size(); ++j) {
            param2.append( slist.at(j).value(4) )
                    .append(",");
        }
//        qDebug()<<"call GenerateDataStruct:"<<param2;
        //ep->callModel("GenerateDataStruct", "(ss)", key.toUtf8().data(), param2.toUtf8().data());
        ep->callModel("ParseSources", "s", param2.toUtf8().data());

        //qDebug()<<keys.size()<<slist.size()<<"Call GenerateDataStruct:"<<key;

    }
}
