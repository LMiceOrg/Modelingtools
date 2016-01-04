#include "stdafx.h"
#include "dialognamespace.h"
#include "ui_dialognamespace.h"
#include <Qsci/qscilexerpython.h>
DialogNamespace::DialogNamespace(const std::vector< std::pair<std::string,std::string> >&l, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DialogNamespace)
{
    ui->setupUi(this);

    nslist = l;
    QString text(tr("# Namespace settings #\n\n"));
    for(size_t i=0; i< nslist.size(); ++i) {
        text.append(tr("%1 = %2\n").arg(nslist[i].first.c_str())
                    .arg(nslist[i].second.c_str()));
    }
    ui->textEdit->setText(text);
    ui->textEdit->setUtf8(true);

    ui->textEdit->setFont(QFont("simson", 14));
//    QsciLexerPython *lex = new QsciLexerPython;
//    ui->textEdit->setLexer(lex);
}

DialogNamespace::~DialogNamespace()
{
    delete ui;
}
