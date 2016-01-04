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
    //update datastruct xml list
    void modelDataStructFiles(const QStringList& sl);

    //Internal use
    void modelDataStructDblClicked(const QModelIndex& index);
signals:
    void currentDataStructChanged(const QString&);
private:
    Ui::OutputWindow *ui;
    QString modelFolder;
};

#endif // OUTPUTWINDOW_H
