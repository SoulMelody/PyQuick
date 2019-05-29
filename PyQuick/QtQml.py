from __future__ import unicode_literals
from functools import partial

from PyQuick.DOtherSide import ffi, lib
from PyQuick.QtCore import QUrl, QObject
from PyQuick.utils import encode_first_arg, str2ptr


def create_callback(id, wrapper, bindedQObject, dosQObject, type_):
    obj = type_()
    bindedQObject[0] = obj._handle
    dosQObject[0] = obj._vptr


@ffi.callback('DeleteDObject')
def delete_callback(id, bindedQObject):
    lib.dos_qobject_delete(bindedQObject[0])


def qmlRegisterType(type_, mod_name, major, minor, type_name):
    """
    qmlRegisterType(type, str, int, int, str, attachedProperties: type = 0) -> int
    """
    new_callback = ffi.callback('CreateDObject')(partial(create_callback, type_=type_))
    return lib.dos_qdeclarative_qmlregistertype(
        ffi.new(
            'const QmlRegisterType *',
            {
                'major': major,
                'minor': minor,
                'uri': str2ptr(mod_name),
                'qml': str2ptr(type_name),
                'staticMetaObject': type_.metaObject()._vptr,
                'createDObject': new_callback,
                'deleteDObject': delete_callback
            }
        )
    )


def qmlRegisterSingletonType(type_, mod_name, major, minor, type_name):
    """
    qmlRegisterSingletonType(type, str, int, int, str) -> int
    """
    return lib.dos_qdeclarative_qmlregistersingletontype(
        ffi.new(
            'const QmlRegisterType *',
            {
                'major': major,
                'minor': minor,
                'uri': str2ptr(mod_name),
                'qml': str2ptr(type_name),
                'staticMetaObject': type_.metaObject()._vptr,
                'createDObject': create_callback,
                'deleteDObject': delete_callback
            }
        )
    )


class QQmlContext(object):
    def __init__(self, vptr):
        self._vptr = vptr

    @encode_first_arg
    def setContextProperty(self, name, value):
        lib.dos_qqmlcontext_setcontextproperty(self._vptr, name, value._vptr)
    
    def baseUrl(self):
        return QUrl(lib.dos_qqmlcontext_baseUrl(self._vptr))

 
class QQmlApplicationEngine(object):
    def __init__(self, *args, **kwargs):
        vptr = lib.dos_qqmlapplicationengine_create()
        self._vptr = ffi.gc(vptr, lib.dos_qqmlapplicationengine_delete)
        if len(args):
            url = args[0]
            self.load(url)

    def load(self, url):
        if not isinstance(url, QUrl):
            # lib.dos_qqmlapplicationengine_load(self._vptr, url)
            url = QUrl(url)
        lib.dos_qqmlapplicationengine_load_url(self._vptr, url._vptr)

    @encode_first_arg
    def loadData(self, data):
        lib.dos_qqmlapplicationengine_load_data(self._vptr, data)

    @encode_first_arg
    def addImportPath(self, path):
        lib.dos_qqmlapplicationengine_add_import_path(self._vptr, path)

    def rootContext(self):
        return QQmlContext(lib.dos_qqmlapplicationengine_context(self._vptr))
    
    def rootObjects(self):
        raise NotImplementedError
    
    @encode_first_arg
    def addImageProvider(self, name, provider):
        lib.dos_qqmlapplicationengine_addImageProvider(self._vptr, name, provider._vptr)
