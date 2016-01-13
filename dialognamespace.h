#ifndef DIALOGNAMESPACE_H
#define DIALOGNAMESPACE_H

#include <QDialog>

namespace Ui {
class DialogNamespace;
}

class DialogNamespace : public QDialog
{
    Q_OBJECT

public:
    DialogNamespace(const QString &name,  QWidget *parent = 0);
    ~DialogNamespace();


private:
    Ui::DialogNamespace *ui;
    QString fileName;
    QsciLexerPython* pyparser;
//    std::vector< std::pair<std::string,std::string> > nslist;
};

#endif // DIALOGNAMESPACE_H
