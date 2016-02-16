#include "stdafx.h"
#include "dialognamespace.h"
#include "ui_dialognamespace.h"
#include <Qsci/qscilexerpython.h>
DialogNamespace::DialogNamespace(const QString &name, EmbedPython *emb, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DialogNamespace)
{
    ui->setupUi(this);
    ep = emb;
    fileName = name;
    pyparser = new QsciLexerPython(this);

//    QString text(tr("# Namespace settings #\n\n"));

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

    QString file = fileName;
    file.replace(qApp->applicationDirPath(), "");
    this->setWindowTitle( this->windowTitle() + tr(" %1").arg(file) );
}

DialogNamespace::~DialogNamespace()
{
    delete ui;
}

void DialogNamespace::on_buttonBox_accepted()
{
    ///1.写回文件
    QFile f(fileName);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text))
        return;
    f.write(ui->textEdit->text().toUtf8());
    f.close();

    QFileInfo info(fileName);

    QString model = info.absoluteFilePath().replace("\\", ".").replace("/", ".");
    QString pattern = "site-packages";
    int pos = model.indexOf(pattern);
    if(pos >= 0) {
        model = model.mid(pos + pattern.length()+1);
    }
    if (model.right(3).compare(".py") == 0) {
        model = model.left( model.size() - 3);
    }

    if(model.right(9).compare(".__init__") == 0) {
        model = model.left( model.size() - 9);
    }
    //QString model = fileName.replace(qApp->applicationDirPath(), "").replace(QDir::separator(), ".");
    //QMessageBox::information(this, qApp->applicationDirPath(), model);
    qDebug()<<model;
    ep->reloadModel(model.toUtf8().data());
}
