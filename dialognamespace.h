#ifndef DIALOGNAMESPACE_H
#define DIALOGNAMESPACE_H

#include <QDialog>
#include "embedpython.h"

namespace Ui {
class DialogNamespace;
}

class DialogNamespace : public QDialog
{
    Q_OBJECT

public:
    DialogNamespace(const QString &name,  EmbedPython *emb = NULL, QWidget *parent = 0);
    ~DialogNamespace();


private slots:
    void on_buttonBox_accepted();

private:
    Ui::DialogNamespace *ui;
    QString fileName;
    QsciLexerPython* pyparser;
    EmbedPython *ep;
//    std::vector< std::pair<std::string,std::string> > nslist;
};

#endif // DIALOGNAMESPACE_H
