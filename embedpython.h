#ifndef EMBEDPYTHON_H
#define EMBEDPYTHON_H

#include <stdarg.h>
#include <string>

//TODO:Python embed helper class
class EmbedPython
{
public:
    EmbedPython();
    ~EmbedPython();

    bool init();
    void finit();
    void reload();

    int callModel(const char *method, const char *format, ...);
    const char* returnType() const;
    PyObject* returnObject() const;
    std::string errorMessage();
    void checkError();
private:
    QByteArray  py_progname;
    QByteArray py_pythonhome;
    PyObject *modeltool;
    PyObject *mainmodel;
    PyObject *retobj;
    PyObject *globals;
    PyObject *locals;
    bool initialized;
    QMutex mutex;
    std::string emsg;

};

#endif // EMBEDPYTHON_H
