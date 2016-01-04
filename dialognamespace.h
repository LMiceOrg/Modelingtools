#ifndef DIALOGNAMESPACE_H
#define DIALOGNAMESPACE_H

#include <QDialog>
#include <vector>
#include <string>

namespace Ui {
class DialogNamespace;
}

class DialogNamespace : public QDialog
{
    Q_OBJECT

public:
    DialogNamespace(const std::vector< std::pair<std::string,std::string> >&l,  QWidget *parent = 0);
    ~DialogNamespace();


private:
    Ui::DialogNamespace *ui;
    std::vector< std::pair<std::string,std::string> > nslist;
};

#endif // DIALOGNAMESPACE_H
