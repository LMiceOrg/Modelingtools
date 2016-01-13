#ifndef OUTPUTWINDOW_H
#define OUTPUTWINDOW_H

#include <QDockWidget>

namespace Ui {
class OutputWindow;
}

class OutputWindow : public QDockWidget
{
    Q_OBJECT

public:
    explicit OutputWindow(QWidget *parent = 0);
    ~OutputWindow();
public slots:
    void modelNameChanged(const QString& title);
    void modelExcelListChanged(const QStringList& sl);
    void modelExcelAddFile(const QString& name);
    void modelExcelRemoveFile(const QString& name);
    //update datastruct xml list
    void modelDataStructFiles(const QStringList& sl);
    void modelModelDscFiles(const QStringList& sl);
    // Model code file
    void modelModelCodeFiles(const QStringList& sl);

    //Internal use
    void modelDataStructDblClicked(const QModelIndex& index);
    void modelModelDscDblClicked(const QModelIndex& index);

signals:
    void currentDataStructChanged(const QString&);
    void currentCodeFileChanged(const QString&);
private slots:
    void on_treeProject_doubleClicked(const QModelIndex &index);

    void on_treeWidget_doubleClicked(const QModelIndex &index);

private:
    Ui::OutputWindow *ui;
    QString modelFolder;
};



#endif // OUTPUTWINDOW_H
