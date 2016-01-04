#include "stdafx.h"
#include "embedpython.h"

#define MODELTOOL "autotools.component_parser_excel"
EmbedPython::EmbedPython()
    :modeltool(NULL), mainmodel(NULL),retobj(NULL),
      globals(NULL),locals(NULL),
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
    QString p = dir.absolutePath()+QString("/python27");
    py_progname = p.toLocal8Bit();

    p = dir.absolutePath() + QString("/embed");
    py_pythonhome = p.toLocal8Bit();

    Py_SetProgramName(py_progname.data());
    Py_SetPythonHome(py_pythonhome.data());

    /** Initialize Python */
    Py_InitializeEx(0);
    if(Py_IsInitialized() != 0) {
        initialized = true;
        globals = PyList_New(0);
        locals = PyList_New(0);
        PyObject* fromlist = PyList_New(1);
        PyList_SET_ITEM(fromlist, 0, PyString_FromString("*"));
        /** Import main module */
        mainmodel = PyImport_ImportModuleEx("__main__", globals, locals, fromlist);

        /** Import modeltool module */
        modeltool = PyImport_ImportModuleEx(MODELTOOL, globals, locals, fromlist);

        Py_XDECREF(fromlist);
    } else {
        qDebug()<<"Init failed";
    }

    return initialized;
}

void EmbedPython::finit()
{
    /** Lock for thread-safe */
    QMutexLocker locker(&mutex);

    if(initialized) {
        Py_XDECREF(retobj);
        Py_XDECREF(modeltool);
        Py_XDECREF(mainmodel);
        modeltool = NULL;
        mainmodel = NULL;
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
            Py_XDECREF(modeltool);
            modeltool = newmodel;
        } else {
            newmodel = PyImport_ImportModule(MODELTOOL);
            modeltool = newmodel;
        }
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
    va_end(vl);

    retobj = PyObject_CallMethodObjArgs(modeltool, md, args, NULL);
    } else {
        retobj = PyObject_CallMethodObjArgs(modeltool, md, NULL);
    }

    // Print error stack
    if(PyErr_Occurred()) {
        PyObject *ptp = NULL, *pv = NULL, *ptb = NULL;
        PyErr_Fetch(&ptp, &pv, &ptb);
        if(ptp && PyType_Check(ptp)) {
            qDebug()<<"error Type:"<<QString(((PyTypeObject*)(ptp))->tp_name);
        }
        if(pv && PyString_Check(pv) ) {
            qDebug()<<"error value:"<<QString(PyString_AsString(pv));
        }
        if(ptb) {

            PyTracebackObject *traceback = ((PyTracebackObject*)ptb);
            for (;traceback ; traceback = traceback->tb_next) {
                PyCodeObject *codeobj = traceback->tb_frame->f_code;
                qDebug()<<QString("%1: %2(# %3)")
                                  .arg(PyString_AsString(codeobj->co_name))
                                  .arg(PyString_AsString(codeobj->co_filename))
                                  .arg(traceback->tb_lineno);
            }
        }
        //PyErr_Print();
    }

    if(retobj) {
        qDebug()<<"return type:"<<retobj->ob_type->tp_name;
    }
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
