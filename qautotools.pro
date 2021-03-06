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
    embedpython.h \
    autotools/builder/ep_hpp_tmpl.h \
    autotools/builder/ed_hpp_tmpl.h \
    autotools/builder/cd_hpp_tmpl.h \
    autotools/builder/pj_hpp_tmpl.h \
    autotools/builder/dp_hpp_tmpl.h \
    autotools/builder/md_hpp_tmpl.h

FORMS    += mainwindow.ui \
    dialognamespace.ui \
    outputwindow.ui

#install python script
pysrc.files=autotools/*
INSTALLS += pysrc

#install translation
trans.files = *.qm
trans.path = $$OUT_PWD/release
INSTALLS += trans

win32-msvc2012 {
message("msvc")
DEFINES += Py_BUILD_CORE
INCLUDEPATH += C:/Python27/include
LIBS += -L"C:/Python27/libs"  -lpython27
pysrc.path = $$OUT_PWD/release/autotools
message($$pysrc.path)
}

win32-g++ {
message("mkspecs=win32-g++")
SYS_TYPE = $$find(QMAKE_QMAKE, msys)
isEmpty(SYS_TYPE) {
message("Mingw build")
INCLUDEPATH += C:/Python27/include
LIBS += -LC:/Python27/libs
LIBS += -lpython27

pysrc.path=$$OUT_PWD/release/Lib/site-packages/autotools

#copy dist to trunk
trunk.path = $$PWD/../../tool/$$TARGET
trunk.files = *.qm
trunk.files += $$OUT_PWD/release/*.exe
INSTALLS += trunk

trunk2.path =  $$PWD/../../tool/$$TARGET/Lib/site-packages/autotools
trunk2.files = autotools/*
INSTALLS += trunk2

}
!isEmpty(SYS_TYPE) {
message("Msys build")

INCLUDEPATH += $$[QT_INSTALL_HEADERS]"/python2.7"
LIBS += -lpython2.7

pysrc.path=$$OUT_PWD/release/Lib/python2.7/site-packages/autotools
}

QMAKE_CXXFLAGS += -std=c++03
QMAKE_CXXFLAGS += -march=native  -Wall -Wextra -Wpedantic

}
macx-clang {

#Boost library
INCLUDEPATH += /opt/local/include

QMAKE_LFLAGS += -F/opt/local/Library/Frameworks
INCLUDEPATH += /opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7
LIBS += -framework Python

pysrc.path = $$OUT_PWD/modelingtools.app/Contents/Resources/site-packages/autotools

#qscintilla2
qsci.path = $$OUT_PWD/modelingtools.app/Contents/MacOS
qsci.files += $$[QT_INSTALL_LIBS]/libqscintilla2.12.dylib

#translation
trans.path = $$OUT_PWD/modelingtools.app/Contents/MacOS
trans.files = *.qm
INSTALLS += trans

INSTALLS += qsci
QMAKE_MACOSX_DEPLOYMENT_TARGET = 10.7
#QMAKE_CXXFLAGS += -std=c++03
QMAKE_CXXFLAGS += -std=c++11
QMAKE_CXXFLAGS += -march=native  -Wall -Wextra -Wpedantic  -stdlib=libc++
#QMAKE_CXXFLAGS += -E

LIBS += -stdlib=libc++
}

LIBS += -lqscintilla2



OTHER_FILES += autotools/*.py \
autotools/modelparser/*.py \
autotools/datamodel/*.py \
autotools/builder/*.py \
autotools/builder/*.cpp \
autotools/builder/*.h \
css/*.css   \
*.ts \
    autotools/builder/pf_ini_tmpl.ini

win32 {
RC_FILE += modelingtools.rc
#RC_ICONS = css/vcsolution.ico

INCLUDEPATH += "C:/Program Files (x86)/appsoft/DWK/V32/SimCEE/include"
DEFINES += _APPSIM_ENUM_DEFINED
DEFINES += __BOOL_DEFINED
}

PRECOMPILED_HEADER += stdafx.h

precompile_header:!isEmpty(PRECOMPILED_HEADER) {
DEFINES += USING_PCH
}

RESOURCES += \
    modelingtools.qrc

DISTFILES += \
    autotools/builder/cppheaderbuilder.py

TRANSLATIONS += modelingtools.zh_CN.ts

