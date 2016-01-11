#-------------------------------------------------
#
# Project created by QtCreator 2015-12-29T01:07:05
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += precompile_header  qscintilla2

TARGET = modelingtools
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

#install python script
pysrc.path=$$OUT_PWD/release/Lib/python2.7/site-packages/autotools
pysrc.files=autotools/*
INSTALLS += pysrc

win32-msvc2012 {
message("msvc")
DEFINES += Py_BUILD_CORE
INCLUDEPATH += C:/Python27/include
LIBS += -L"C:/Python27/libs"  -lpython27
pysrc.path = $$OUT_PWD/release/autotools
message($$pysrc.path)
}

win32-g++ {
INCLUDEPATH += $$[QT_INSTALL_HEADERS]"/python2.7"
LIBS += -lpython2.7.dll

}
macx-clang {

#Boost library
INCLUDEPATH += /opt/local/include

QMAKE_LFLAGS += -F/opt/local/Library/Frameworks
INCLUDEPATH += /opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7
LIBS += -framework Python

pysrc.path = $$OUT_PWD/modelingtools.app/Contents/Resources/autotools

#qscintilla2
qsci.path = $$OUT_PWD/modelingtools.app/Contents/MacOS
qsci.files += $$[QT_INSTALL_LIBS]/libqscintilla2.12.dylib

INSTALLS += qsci

QMAKE_CXXFLAGS += -march=native -std=c++11 -Wall -Wextra -Wpedantic
}

LIBS += -lqscintilla2



OTHER_FILES += autotools/*.py \
autotools/modelparser/*.py \
autotools/datamodel/*.py \
autotools/builder/*.py \
css/*.css \
    autotools/builder/msvc2008builder.py \
    autotools/builder/msvc2008solutionbuilder.py \
    autotools/builder/msvc2008projectbuilder.py \
    autotools/builder/qt5builder.py

PRECOMPILED_HEADER += stdafx.h

precompile_header:!isEmpty(PRECOMPILED_HEADER) {
DEFINES += USING_PCH
}

RESOURCES += \
    modelingtools.qrc

DISTFILES += \
    autotools/builder/cppheaderbuilder.py


