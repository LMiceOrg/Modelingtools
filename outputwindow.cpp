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

    ui->tabWidget->setTabText(0, tr("Project"));
    ui->tabWidget->setTabText(1, tr("Data Structure"));

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
                    root->child(j)->addChild(new
                                             QTreeWidgetItem(root->child(j),
                                                             QStringList(xlfile)) );
                    inserted= true;
                    break;//for-j
                }
            }
            if(!inserted) {
                QTreeWidgetItem* path = new QTreeWidgetItem(root,
                                                            QStringList(xlpath) );
                path->addChild(new QTreeWidgetItem(path, QStringList(xlfile)));
                root->addChild(path);
            }
        } else { //path is empty

            root->addChild(new
                           QTreeWidgetItem(root,
                                           QStringList(xlfile) ) );
        }
    }
    ui->treeWidget->expandAll();
}

void OutputWindow::modelDataStructFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeDataStruct;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xmlfile = info.fileName();
        root->addChild(new QTreeWidgetItem(root, QStringList( xmlfile )) );
    }
    tree->expandAll();

}

void OutputWindow::modelDataStructDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data().toString() );
}
