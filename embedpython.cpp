#include "stdafx.h"
#include "embedpython.h"

///** Lock for thread-safe */
//QMutexLocker locker(&mutex);
//#define MODELTOOL "autotools.component_parser_excel"
#define MODELTOOL "autotools.modelingtools"
EmbedPython::EmbedPython(QObject *parent)
    :QObject(parent), modeltool(NULL), retobj(NULL),
      //globals(NULL),locals(NULL),
      initialized(false)
{
    init();
}

EmbedPython::~EmbedPython()
{
    finit();
}

bool EmbedPython::init()
{

    if(initialized)
        return true;

    /** Setting Python folder */
    QDir dir(qApp->applicationDirPath());
    //
    QString p = QString("python27");
    py_progname = p.toLocal8Bit();

#if __APPLE__
    dir.cdUp();
    dir.cd("Resources");
#endif

    p = dir.absolutePath();// + dir.separator() + QString("embed");

    py_pythonhome = p.toLocal8Bit();
    //QMessageBox::warning(NULL, "", p);

#if !__APPLE__
    Py_SetProgramName(py_progname.data());
//    qDebug()<<"program path:"<<Py_GetProgramFullPath();
//    qDebug()<<"program name:"<<Py_GetProgramName();
//    qDebug()<<"python path:"<<Py_GetPath() ;
    Py_SetPythonHome(py_pythonhome.data());
#endif
//    qDebug()<<"program home:"<<Py_GetPythonHome();
//    qDebug()<<"program path:"<<Py_GetProgramFullPath();
//    qDebug()<<"program name:"<<Py_GetProgramName();
//    qDebug()<<"python path:"<<Py_GetPath() ;
//    QMessageBox::warning(NULL, "", Py_GetPath());
    /** Initialize Python */
    Py_InitializeEx(0);
    //Py_Initialize();
    if(Py_IsInitialized() != 0) {
        initialized = true;
        //globals = PyList_New(0);
        //locals = PyList_New(0);
//        PyObject* fromlist = PyList_New(1);
//        PyList_SET_ITEM(fromlist, 0, PyString_FromString("*"));
        /** Import main module */
//        char mname[512];
//        memset(mname, 0, 512);
//        memcpy(mname, "__main__", sizeof("__main__"));
//        mainmodel = PyImport_ImportModuleEx(mname, globals, locals, fromlist);
//        checkError();
        /** Import modeltool module */
//        memset(mname, 0, 512);
//        memcpy(mname, MODELTOOL, sizeof(MODELTOOL));
        //modeltool = PyImport_ImportModuleEx(mname, globals, locals, fromlist);
        QString cmd = QString("import sys; import os;  sys.path.append(os.path.abspath('%1'))")
#if __APPLE__
                .arg(dir.absolutePath());
#else
                .arg(qApp->applicationDirPath());
#endif
        PyRun_SimpleString(cmd.toLocal8Bit().data());
        checkError();
        modeltool = PyImport_ImportModule(MODELTOOL);
//        qDebug()<<"imported modeltool";
//        PyErr_Print();
        checkError();
//        qDebug()<<"import and checked error";
//        if(!modeltool) {
//            initialized = false;
//        }
//        Py_XDECREF(fromlist);
//    } else {
//        qDebug()<<"Init failed";
    }

    return initialized;
}

void EmbedPython::finit()
{

    if(initialized) {
        Py_XDECREF(retobj);
        //Py_XDECREF(globals);
        //Py_XDECREF(locals);
        Py_XDECREF(modeltool);
        //Py_XDECREF(mainmodel);
        modeltool = NULL;
        //mainmodel = NULL;
        retobj = NULL;
        Py_Finalize();
    }
}

void EmbedPython::reload()
{

    if(initialized) {
        PyObject* newmodel = NULL;
        /** Import modeltool module */
        if(modeltool) {
            newmodel = PyImport_ReloadModule(modeltool);
            checkError();
            Py_XDECREF(modeltool);
            modeltool = newmodel;
        } else {
            newmodel = PyImport_ImportModule(MODELTOOL);
            checkError();
            modeltool = newmodel;
        }

        callModel("Init", NULL);
        checkError();
    }
}


int EmbedPython::callModel(const char *method, const char *format, ...)
{
    PyObject *args = NULL;
    PyObject *md = NULL;
    va_list vl;

    Py_XDECREF(retobj);
    retobj = NULL;

    if(!modeltool)
        return 1;

    md = PyString_FromString(method);
    //qDebug()<<"method type is :"<<md->ob_type->tp_name;

    if(format) {
        va_start(vl, format);
        args = Py_VaBuildValue(format, vl);
        checkError();
        va_end(vl);

        retobj = PyObject_CallMethodObjArgs(modeltool, md, args, NULL);
    } else {
        retobj = PyObject_CallMethodObjArgs(modeltool, md, NULL);
    }

    checkError();
//    PyErr_Print();


//    if(retobj) {
//        qDebug()<<"return type:"<<retobj->ob_type->tp_name;
//    }
    Py_XDECREF(args);
    Py_XDECREF(md);


    return 0;
}

const char *EmbedPython::returnType() const
{
    if(!retobj)
        return NULL;
    return retobj->ob_type->tp_name;
}

PyObject *EmbedPython::returnObject() const
{
    return retobj;
}

QString EmbedPython::errorMessage() const
{
    return emsg;
}

class PyObjectToMessage
{
public:
    PyObjectToMessage(QString& msg)
        :emsg(msg)
    {}


    void PyObjectToMessageString(PyObject* pv) {
        if(!pv)
            return;

        if(PyString_Check(pv)) {
            errvals.push_back( PyString_AsString(pv) );
        } else if (PyTuple_Check(pv)) {
            TupleToMessageString(pv);
        } else if( PyList_Check(pv)) {
            ListToMessageString(pv);
        } else if(PyInt_Check(pv)) {
            char buf[128] = {0};
            sprintf(buf, " %ld", PyInt_AS_LONG(pv));
            errvals.push_back(  buf );
        }else{
            qDebug()<<"not parse type:"<<pv->ob_type->tp_name;
        }
    }

    void TupleToMessageString(PyObject* pv) {
        for(Py_ssize_t i=0; i< PyTuple_Size(pv); ++i) {
            PyObject* val = PyTuple_GetItem(pv, i);
            PyObjectToMessageString(val);
        }
    }

    void ListToMessageString(PyObject* pv) {
        for(Py_ssize_t i=0; i< PyList_Size(pv); ++i) {
            PyObject* val = PyList_GetItem(pv, i);
            PyObjectToMessageString(val);
        }
    }

    QString& emsg;
    std::vector<std::string> errvals;

};

void EmbedPython::checkError()
{
    // Print error stack
    if(PyErr_Occurred()) {
        emsg.clear();
//        PyErr_Print();
//        qDebug()<<"1";
        PyObject *ptp = NULL, *pv = NULL, *ptb = NULL;
        PyErr_Fetch(&ptp, &pv, &ptb);
//        qDebug()<<"2";
        if(ptp && PyType_Check(ptp)) {
//            qDebug()<<"2.1";
            emsg += tr("Error Type:%1\n")
                    .arg(((PyTypeObject*)(ptp))->tp_name);
        }


        if(ptb) {

//            qDebug()<<"3";

            PyTracebackObject *traceback = ((PyTracebackObject*)ptb);
            for (;traceback ; traceback = traceback->tb_next) {
                PyCodeObject *codeobj = traceback->tb_frame->f_code;
                emsg += tr("  %1: %2(# %3)\n")
                        .arg(PyString_AsString(codeobj->co_name))
                        .arg(PyString_AsString(codeobj->co_filename))
                        .arg(traceback->tb_lineno);
            }
        }

        if(pv && PyString_Check(pv) ) {
//            qDebug()<<"2.2";
            emsg += tr("  Error Value:%1\n")
                    .arg( PyString_AsString(pv) );

            //qDebug()<<"Error Value: emsg.c_str():"<<pv->ob_type->tp_name;
        } else if(pv && PyUnicode_Check(pv)) {
            emsg += tr("  Error Value:%1\n")
                    .arg( tr("Unicode error") );
        }else if(pv && PyTuple_Check(pv)) {
//            qDebug()<<"2.3"<<pv->ob_type->tp_name;
//            if( PyString_Check( ((PyBaseExceptionObject*)(pv))->message) ) {
////
//                emsg += tr("  Error Value:%1\n")
//                        .arg( PyString_AsString( ((PyBaseExceptionObject*)(pv))->message ) );
//            }
            QString msgval = tr(" Error value: ");
            PyObjectToMessage tm(msgval);
            tm.PyObjectToMessageString(pv);
            qDebug()<<"size:"<<tm.errvals.size();
            if(tm.errvals.size() == 5) {
                emsg += tr("Files: %2 (%3) \n %5 %1: %4\n")
                        .arg(tm.errvals[0].c_str())
                        .arg(tm.errvals[1].c_str())
                        .arg(tm.errvals[2].c_str())
                        .arg(tm.errvals[3].c_str())
                        .arg(tm.errvals[4].c_str());
            }

        }

        PyErr_Print();
        emit errorTrigger(emsg);

    }

}
