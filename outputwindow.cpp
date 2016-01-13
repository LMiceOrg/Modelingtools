#include "stdafx.h"
#include "outputwindow.h"
#include "ui_outputwindow.h"

#include <QProcess>

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



    QPixmap px(":/flatastic1");
    int px_width = 112, px_height = 112;
    ui->tabWidget->setTabText(0, tr("Project"));
    ui->tabWidget->setTabText(1, tr("Data Structure"));
    ui->tabWidget->setTabText(2, tr("Model Description"));
    ui->tabWidget->setTabText(3, tr("Model Code"));
    ui->tabWidget->setTabIcon(0, QIcon(px.copy(0*px_width,3*px_height,  px_width,px_height)));
    ui->tabWidget->setTabIcon(1, QIcon(px.copy(3*px_width,3*px_height,  px_width,px_height)));
    ui->tabWidget->setTabIcon(2, QIcon(px.copy(4*px_width,0*px_height,  px_width,px_height)));
    ui->tabWidget->setTabIcon(3, QIcon(px.copy(1*px_width,0*px_height,  px_width,px_height)));



    modelFolder = qApp->applicationDirPath();

    QTreeWidget* tree;
    QTreeWidgetItem* item;
    QStringList ls;

    tree = ui->treeWidget;
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model Excel File"));

    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

    tree = ui->treeDataStruct;
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model Data Structure"));

    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

    tree = ui->treeModelDsc;
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model Description"));

    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);

    tree = ui->treeProject;
    tree->setColumnCount(1);
    tree->setHeaderLabel(tr("Model Code"));

    tree->insertTopLevelItem(0, new QTreeWidgetItem(tree, ls));
    item = tree->topLevelItem(0);
    item->setChildIndicatorPolicy(QTreeWidgetItem::DontShowIndicatorWhenChildless);
}

OutputWindow::~OutputWindow()
{
    delete ui;
}

void OutputWindow::modelNameChanged(const QString &title)
{
    QTreeWidget* tree;
    QTreeWidgetItem* item;

    modelFolder = title;

    tree = ui->treeWidget;

    item = tree->topLevelItem(0);
    item->takeChildren();
    item->setText(0, title);

    tree = ui->treeDataStruct;
    item = tree->topLevelItem(0);
    item->takeChildren();
    item->setText(0, title);

    tree = ui->treeModelDsc;
    item = tree->topLevelItem(0);
    item->takeChildren();
    item->setText(0, title);

    tree = ui->treeProject;
    item = tree->topLevelItem(0);
    item->takeChildren();
    item->setText(0, title);


}

void OutputWindow::modelExcelListChanged(const QStringList &sl)
{
    QTreeWidget* tree = ui->treeWidget;
    QTreeWidgetItem* root = tree->topLevelItem(0);

    //Remove and return children list
    root->takeChildren();

    for(int i=0; i<sl.size(); ++i) {
        modelExcelAddFile(sl.at(i));
    }
    tree->expandAll();
}

void OutputWindow::modelExcelAddFile(const QString &name)
{
    QTreeWidget* tree = ui->treeWidget;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    QPixmap px(":/flatastic1");
    const int px_width = 112, px_height = 112;

    QFileInfo info(name);
    QString xlpath = info.absolutePath().replace(modelFolder, tr(""));

    QString xlfile = info.fileName();
    if(xlpath.compare("")!=0) {
        bool inserted = false;
        for(int j = 0; j<root->childCount(); ++j) {
            if(root->child(j)->text(0).compare(xlpath, Qt::CaseInsensitive) == 0) {
                QTreeWidgetItem* item = new QTreeWidgetItem(
                                   root->child(j),
                                   QStringList(xlfile));
                item->setIcon(0, QIcon(px.copy(4*px_width,2*px_height,  px_width,px_height)));
                item->setData(0, Qt::UserRole, info.absoluteFilePath());
                inserted= true;
                break;//for-j
            }
        }
        if(!inserted) {
            QTreeWidgetItem* path = new QTreeWidgetItem(
                        root,
                        QStringList(xlpath) );
            //path->setIcon(0, style()->standardIcon(QStyle::SP_DirIcon));
            path->setIcon(0, QIcon(px.copy(4*px_width,4*px_height,  px_width,px_height)));
            QTreeWidgetItem* item = new QTreeWidgetItem(
                               path,
                               QStringList(xlfile));
            //item->setIcon(0, style()->standardIcon(QStyle::SP_FileIcon) );
            item->setIcon(0, QIcon(px.copy(4*px_width,2*px_height,  px_width,px_height)));
            item->setData(0, Qt::UserRole, info.absoluteFilePath());
//                root->addChild(path);
        }
    } else { //path is empty

        QTreeWidgetItem* item =new QTreeWidgetItem(
                           root,
                           QStringList(xlfile) );
        item->setData(0, Qt::UserRole, info.absoluteFilePath());
    }
}

void OutputWindow::modelExcelRemoveFile(const QString &name)
{
    QTreeWidget* tree = ui->treeWidget;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    QFileInfo info(name);
    QString xlpath = info.absolutePath().replace(modelFolder, tr(""));
    QString xlfile = info.fileName();

    bool removed = false;
    for(int j = 0; j<root->childCount(); ++j) {
        if(root->child(j)->text(0).compare(xlpath, Qt::CaseInsensitive) == 0) {
            QTreeWidgetItem* item = root->child(j);
            for(int k = 0; k< item->childCount(); ++k) {
                if( item->child(k)->text(0).compare(xlfile, Qt::CaseInsensitive) == 0) {
                    //Gotcha!
                    item->takeChild(k);
                    removed = true;
                    break;//for-k
                }
            }
            if(removed) {
                if( item->childCount() == 0) {
                    root->takeChild(j);
                }
                break;//for-j
            }
        } else if(root->child(j)->text(0).compare(xlfile, Qt::CaseInsensitive) == 0) {
            root->takeChild(j);
            break;//for-j
        }
    }

}


void OutputWindow::modelDataStructFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeDataStruct;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    QPixmap px(":/flatastic1");
    int px_width = 112, px_height = 112;
    //Remove and return children list
    root->takeChildren();

    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xmlfile = info.fileName();
        QTreeWidgetItem* item = new QTreeWidgetItem(root, QStringList( xmlfile ));
//        item->setIcon(0, style()->standardIcon(QStyle::SP_DriveNetIcon));
        item->setIcon(0, QIcon(px.copy(1*px_width,2*px_height,  px_width,px_height)));
        item->setData(0, Qt::UserRole, info.absoluteFilePath() );
    }
    tree->expandAll();

}

void OutputWindow::modelModelDscFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeModelDsc;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    QPixmap px(":/flatastic1");
    int px_width = 112, px_height = 112;
    //Remove and return children list
    root->takeChildren();

    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xmlfile = info.fileName();
        QTreeWidgetItem* item = new QTreeWidgetItem(root, QStringList( xmlfile ));
//        item->setIcon(0, style()->standardIcon(QStyle::SP_DriveCDIcon));
        item->setIcon(0, QIcon(px.copy(0*px_width,1*px_height,  px_width,px_height)));
        item->setData(0, Qt::UserRole, info.absoluteFilePath() );
//        root->addChild(new QTreeWidgetItem(root, QStringList( xmlfile )) );
    }
    tree->expandAll();
}

QString GetIcon(const QString& file) {
    //qDebug()<<file;
    if ( file.endsWith(".h") || file.endsWith(".hpp") ) {
        return ":/icon/css/headerfile.ico";
    } else if(file.endsWith(".cpp") || file.endsWith(".c") ) {
        return ":/icon/css/cplusplus.ico";
    } else if(file.endsWith(".pro") ) {
        return ":/icon/css/qtproject.ico";
    } else if(file.endsWith(".sln") ) {
        return ":/icon/css/vcsolution.ico";
    } else if(file.endsWith(".vcproj") ) {
        return ":/icon/css/vcproject.ico";
    } else {
        return ":/icon/css/xmldoc.ico";
    }

}

void OutputWindow::modelModelCodeFiles(const QStringList &sl)
{
    QTreeWidget * tree = ui->treeProject;
    QTreeWidgetItem* root = tree->topLevelItem(0);
    //Remove and return children list
    root->takeChildren();

    for(int i=0; i<sl.size(); ++i) {
        QFileInfo info(sl.at(i));
        QString xlpath = info.absolutePath().replace(modelFolder, tr(""));

        QString xlfile = info.fileName();
        if(xlpath.compare("")!=0) {
            bool inserted = false;
            for(int j = 0; j<root->childCount(); ++j) {
                if(root->child(j)->text(0).compare(xlpath, Qt::CaseInsensitive) == 0) {
                    QTreeWidgetItem* item = new QTreeWidgetItem(
                                       root->child(j),
                                       QStringList(xlfile));
                    item->setIcon(0, QIcon( GetIcon(xlfile) ));
                    item->setData(0, Qt::UserRole, info.absoluteFilePath() );
//                    item->setIcon(0, style()->standardIcon(QStyle::SP_FileIcon) );
                    inserted= true;
                    break;//for-j
                }
            }
            if(!inserted) {
                QTreeWidgetItem* path = new QTreeWidgetItem(
                            root,
                            QStringList(xlpath) );
                path->setIcon(0, style()->standardIcon(QStyle::SP_DirIcon));
                //path->setIcon(0, QIcon(px.copy(4*px_width,4*px_height,  px_width,px_height)));
                QTreeWidgetItem* item = new QTreeWidgetItem(
                                   path,
                                   QStringList(xlfile));
                //item->setIcon(0, style()->standardIcon(QStyle::SP_FileIcon) );
                item->setIcon(0, QIcon( GetIcon(xlfile) ));
                item->setData(0, Qt::UserRole, info.absoluteFilePath() );
//                root->addChild(path);
            }
        } else { //path is empty


            QTreeWidgetItem* item = new QTreeWidgetItem(
                               root,
                               QStringList(xlfile));
            item->setIcon(0, QIcon( GetIcon(xlfile) ));
            item->setData(0, Qt::UserRole, info.absoluteFilePath() );
        }
    }
    tree->expandAll();
}

void OutputWindow::modelDataStructDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data(Qt::UserRole).toString() );
}

void OutputWindow::modelModelDscDblClicked(const QModelIndex &index)
{
    emit currentDataStructChanged( index.data(Qt::UserRole).toString() );
}

//view Model code file
void OutputWindow::on_treeProject_doubleClicked(const QModelIndex &index)
{
    emit currentCodeFileChanged(index.data(Qt::UserRole).toString());
}

void OutputWindow::on_treeWidget_doubleClicked(const QModelIndex &index)
{
    QString name = index.data(Qt::UserRole).toString();
    if(name.isEmpty())
        return;

    name = "open " + name;

     QProcess::startDetached(name);
}
