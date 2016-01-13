#include "stdafx.h"
#include "dialognamespace.h"
#include "ui_dialognamespace.h"
#include <Qsci/qscilexerpython.h>
DialogNamespace::DialogNamespace(const QString &name, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DialogNamespace)
{
    ui->setupUi(this);

    fileName = name;
    pyparser = new QsciLexerPython(this);

    QString text(tr("# Namespace settings #\n\n"));

    QFile f(fileName);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
        return;
    QString ctx = QString(f.readAll());
    f.close();
    ui->textEdit->setUtf8(true);
    ui->textEdit->setText(ctx);
    ui->textEdit->setAutoIndent(true);

    ui->textEdit->setLexer(pyparser);
    ui->textEdit->setFolding(QsciScintilla::BoxedTreeFoldStyle);
    // Show line number in left side
    ui->textEdit->setMarginLineNumbers(QsciScintilla::SC_MARGIN_NUMBER, true);
    ui->textEdit->setMarginWidth(QsciScintilla::SC_MARGIN_NUMBER, 32);

    ui->textEdit->setFont(QFont("simson", 14));
//    QsciLexerPython *lex = new QsciLexerPython;
//    ui->textEdit->setLexer(lex);
}

DialogNamespace::~DialogNamespace()
{
    delete ui;
}
