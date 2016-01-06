#include "stdafx.h"
#include "embedpython.h"

#define MODELTOOL "autotools.component_parser_excel"
EmbedPython::EmbedPython()
    :modeltool(NULL), retobj(NULL),
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
    /** Lock for thread-safe */
    QMutexLocker locker(&mutex);

    if(initialized)
        return true;

    /** Setting Python folder */
    QDir dir(qApp->applicationDirPath());
    dir.cdUp();
    dir.cd("Debug");
    //
    QString p = QString("python27");
    py_progname = p.toLocal8Bit();

    dir.cd("embed");

    p = dir.absolutePath();// + dir.separator() + QString("embed");
    py_pythonhome = p.toLocal8Bit();
    //QMessageBox::warning(NULL, "", p);


    Py_SetProgramName(py_progname.data());
//    qDebug()<<"program path:"<<Py_GetProgramFullPath();
//    qDebug()<<"program name:"<<Py_GetProgramName();
//    qDebug()<<"python path:"<<Py_GetPath() ;
    Py_SetPythonHome(py_pythonhome.data());

//    qDebug()<<"program home:"<<Py_GetPythonHome();
//    qDebug()<<"program path:"<<Py_GetProgramFullPath();
//    qDebug()<<"program name:"<<Py_GetProgramName();
//    qDebug()<<"python path:"<<Py_GetPath() ;
    QMessageBox::warning(NULL, "", Py_GetPath());
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
        modeltool = PyImport_ImportModule(MODELTOOL);
        checkError();
//        Py_XDECREF(fromlist);
//    } else {
//        qDebug()<<"Init failed";
    }

    return initialized;
}

void EmbedPython::finit()
{
    /** Lock for thread-safe */
    QMutexLocker locker(&mutex);

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
    /** Lock for thread-safe */
    QMutexLocker locker(&mutex);

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

std::string EmbedPython::errorMessage()
{
    std::string e = emsg;
    emsg.clear();
    return e;
}

void EmbedPython::checkError()
{
    // Print error stack
    if(PyErr_Occurred()) {
        //PyErr_Print();
        PyObject *ptp = NULL, *pv = NULL, *ptb = NULL;
        PyErr_Fetch(&ptp, &pv, &ptb);
        if(ptp && PyType_Check(ptp)) {
            emsg += "Error Type:";
            emsg += ((PyTypeObject*)(ptp))->tp_name;
            emsg +="\n";
        }
        if(pv && PyString_Check(pv) ) {
            emsg += "  Error Value:";
            emsg += PyString_AsString(pv);
            emsg +="\n";
            //qDebug()<<"Error Value: emsg.c_str():"<<pv->ob_type->tp_name;
        } else if(pv) {
            emsg += "  Error Value:";
            emsg += PyString_AsString( ((PyBaseExceptionObject*)(pv))->message );
            emsg += "\n";
        }

        if(ptb) {

            PyTracebackObject *traceback = ((PyTracebackObject*)ptb);
            char fmtmsg [512];
            for (;traceback ; traceback = traceback->tb_next) {
                PyCodeObject *codeobj = traceback->tb_frame->f_code;
                memset(fmtmsg, 0, 512);
                sprintf(fmtmsg,
                        "  %s: %s(# %d)\n",
                        PyString_AsString(codeobj->co_name),
                        PyString_AsString(codeobj->co_filename),
                        traceback->tb_lineno
                        );
                emsg +=fmtmsg;
            }
        }

    }

}
