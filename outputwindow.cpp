#include "stdafx.h"
#include "outputwindow.h"
#include "ui_outputwindow.h"

OutputWindow::OutputWindow(QWidget *parent) :
    QDockWidget(parent),
    ui(new Ui::OutputWindow)
{
    ui->setupUi(this);
    setAllowedAreas(Qt::AllDockWidgetAreas);

    connect(ui->treeDataStruct, SIGNAL(doubleClicked(QModelIndex)),
            this, SLOT(modelDataStructDblClicked(QModelIndex)) );

    connect(ui->treeModelDsc, SIGNAL(doubleClicked(QModelIndex)),
            this, SLOT(modelModelDscDblClicked(QModelIndex)) );

    ui->tabWidget->setTabText(0, tr("Project"));
    ui->tabWidget->setTabText(1, tr("Data Structure"));
    ui->tabWidget->setTabText(2, tr("Model Description"));

    QTreeWidget* tree;
    tree = ui->treeWidget;
    tree->clear();
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model folder:"));
}

OutputWindow::~OutputWindow()
{
    delete ui;
}

void OutputWindow::modelNameChanged(const QString &title)
{
    QTreeWidget* tree;
    modelFolder = title;
    tree = ui->treeWidget;
    tree->clear();
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model Excel File"));
    QStringList ls(modelFolder);

    ui->treeWidget->insertTopLevelItem(0, new QTreeWidgetItem(ui->treeWidget, ls));
    QTreeWidgetItem* item;
    item = ui->treeWidget->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

    //data struct
    ls.clear();
    ls.append(qApp->applicationDirPath());
    tree = ui->treeDataStruct;
    tree->clear();
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Data structure files") );
    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

//    ls.clear();
//    ls.append(qApp->applicationDirPath());
    tree = ui->treeModelDsc;
    tree->clear();
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model description files") );
    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);


}

void OutputWindow::modelExcelListChanged(const QStringList &sl)
{
    QTreeWidgetItem* root = ui->treeWidget->topLevelItem(0);

    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
//        QString st = info.absoluteFilePath();
//        st.replace(modelFolder, tr(""));
        QString xlpath = info.absolutePath().replace(modelFolder, tr(""));

        QString xlfile = info.fileName();
        if(xlpath.compare("")!=0) {
            bool inserted = false;
            for(int j = 0; j<root->childCount(); ++j) {
                if(root->child(j)->text(0).compare(xlpath, Qt::CaseInsensitive) == 0) {
                    QTreeWidgetItem* item = new QTreeWidgetItem(
                                       root->child(j),
                                       QStringList(xlfile));
                    item->setIcon(0, style()->standardIcon(QStyle::SP_FileIcon) );
//                    root->child(j)->addChild(new QTreeWidgetItem(
//                                                 style()->standardIcon(QStyle::SP_FileIcon),
//                                                 root->child(j),
//                                                 QStringList(xlfile)) );
                    inserted= true;
                    break;//for-j
                }
            }
            if(!inserted) {
                QTreeWidgetItem* path = new QTreeWidgetItem(
                            root,
                            QStringList(xlpath) );
                path->setIcon(0, style()->standardIcon(QStyle::SP_DirIcon));
                QTreeWidgetItem* item = new QTreeWidgetItem(
                                   path,
                                   QStringList(xlfile));
                item->setIcon(0, style()->standardIcon(QStyle::SP_FileIcon) );
//                root->addChild(path);
            }
        } else { //path is empty

            root->addChild(new QTreeWidgetItem(
                               root,
                               QStringList(xlfile) ) );
        }
    }
    ui->treeWidget->expandAll();
}

void OutputWindow::modelDataStructFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeDataStruct;
    QTreeWidgetItem* root = tree->topLevelItem(0);

    //Remove and return children list
    root->takeChildren();

    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xmlfile = info.fileName();
        QTreeWidgetItem* item = new QTreeWidgetItem(root, QStringList( xmlfile ));
        item->setIcon(0, style()->standardIcon(QStyle::SP_DriveNetIcon));
    }
    tree->expandAll();

}

void OutputWindow::modelModelDscFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeModelDsc;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xmlfile = info.fileName();
        QTreeWidgetItem* item = new QTreeWidgetItem(root, QStringList( xmlfile ));
        item->setIcon(0, style()->standardIcon(QStyle::SP_DriveCDIcon));
//        root->addChild(new QTreeWidgetItem(root, QStringList( xmlfile )) );
    }
    tree->expandAll();
}

void OutputWindow::modelDataStructDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data().toString() );
}

void OutputWindow::modelModelDscDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data().toString() );
}
