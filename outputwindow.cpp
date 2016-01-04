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
    tree->setHeaderLabel(tr("Model folder:%1").arg(modelFolder));
    QStringList ls(tr("Excel files"));

    ui->treeWidget->insertTopLevelItem(0, new QTreeWidgetItem(ui->treeWidget, ls));
    QTreeWidgetItem* item;
    item = ui->treeWidget->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

    //data struct
    tree = ui->treeDataStruct;
    tree->clear();
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model folder:%1").arg(modelFolder) );
    ls.clear();
    ls.append(tr("Data structure files"));
    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);


}

void OutputWindow::modelExcelListChanged(const QStringList &sl)
{
    QTreeWidgetItem* root = ui->treeWidget->topLevelItem(0);

    for(int i=0; i<sl.size(); ++i) {
        QString st = QDir(sl.at(0)).absolutePath();
        st.replace(modelFolder, tr(""));

        root->addChild(new
                       QTreeWidgetItem(root,
                                       QStringList(st) ) );
    }
    ui->treeWidget->expandAll();
}

void OutputWindow::modelDataStructFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeDataStruct;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    for(int i=0; i<sl.size(); ++i) {
        root->addChild(new QTreeWidgetItem(root, QStringList(sl.at(i) )) );
    }
    tree->expandAll();

}

void OutputWindow::modelDataStructDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data().toString() );
}
