#-------------------------------------------------
#
# Project created by QtCreator 2015-12-29T01:07:05
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += precompile_header

TARGET = qautotools
TEMPLATE = app
#LANGUAGE  = C++

SOURCES += main.cpp\
        mainwindow.cpp \
    dialognamespace.cpp \
    stdafx.cpp \
    outputwindow.cpp \
    embedpython.cpp

HEADERS  += mainwindow.h \
    dialognamespace.h \
    stdafx.h \
    outputwindow.h \
    embedpython.h

FORMS    += mainwindow.ui \
    dialognamespace.ui \
    outputwindow.ui
win32-msvc {
INCLUDEPATH += C:/Python27/include
LIBS += -LC:/Python27/libs  -lpython27
}

win32-g++ {
INCLUDEPATH += $$[QT_INSTALL_HEADERS]"/python2.7"
LIBS += -lpython2.7.dll

}

LIBS += -lqscintilla2
#LIBS += -lpython2.7

#install python script
pysrc.path=$$OUT_PWD/release/Lib/python2.7/site-packages/autotools
pysrc.files=autotools/*
INSTALLS += pysrc

OTHER_FILES += autotools/*.py \
autotools/modelparser/*.py \
autotools/datamodel/*.py \
autotools/builder/*.py

PRECOMPILED_HEADER += stdafx.h

precompile_header:!isEmpty(PRECOMPILED_HEADER) {
DEFINES += USING_PCH
}

message($$OUT_PWD)
