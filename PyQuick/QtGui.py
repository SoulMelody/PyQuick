from six import string_types, ensure_binary

from PyQuick.DOtherSide import ffi, lib
from PyQuick.QtCore import QCoreApplication
from PyQuick.utils import encode_first_arg


class QPixmap(object):
    def __init__(self, *args):
        if len(args) == 0:
            ptr = lib.dos_qpixmap_create()
        elif len(args) == 1 and isinstance(args[0], QPixmap):
            ptr = lib.dos_qpixmap_create_qpixmap(args[0]._vptr)
        elif len(args) == 1 and isinstance(args[0], ffi.CData):
            ptr = args[0]
        elif len(args) == 1 and isinstance(args[0], string_types):
            ptr = lib.dos_qpixmap_create()
        elif len(args) == 2:
            width, height = args
            ptr = lib.dos_qpixmap_create_width_and_height(width, height)
        else:
            raise TypeError('QPixmap(): argument 1 has unexpected type {0!r}'.format(type(args[0]).__name__))
        if len(args) == 1 and isinstance(args[0], ffi.CData):
            self._vptr = ptr
        else:
            self._vptr = ffi.gc(ptr, lib.dos_qpixmap_delete)
        if len(args) == 1 and isinstance(args[0], string_types):
            self.load(args[0])
    
    @encode_first_arg
    def load(self, source, format=''):
        format = ensure_binary(format)
        lib.dos_qpixmap_load(self._vptr, source, format)
        return True

    @encode_first_arg
    def loadFromData(self, data, format=''):
        lib.dos_qpixmap_loadFromData(self._vptr, data, len(data))
        return True

    def fill(self, color):
        red, green, blue, alpha = color
        lib.dos_qpixmap_fill(self._vptr, red, green, blue, alpha)
    
    def isNull(self):
        return lib.dos_qpixmap_isNull(self._vptr)


class QGuiApplication(QCoreApplication):
    def __init__(self, argv=None):
        lib.dos_qguiapplication_create()
    
    def __del__(self):
        lib.dos_qguiapplication_delete()
    
    def exec_(self):
        lib.dos_qguiapplication_exec()

    def quit(self):
        lib.dos_qguiapplication_quit()

