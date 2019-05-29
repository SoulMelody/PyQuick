from enum import IntEnum
from six import ensure_text, add_metaclass
from abc import ABCMeta, abstractmethod

from PyQuick.DOtherSide import ffi, lib
from PyQuick.QtCore import QUrl
from PyQuick.QtGui import QPixmap
from PyQuick.QtQml import QQmlContext
from PyQuick.utils import decode_cstring, ptr2str


@add_metaclass(ABCMeta)
class QQuickImageProvider(object):
    
    class ImageType(IntEnum):
        Image = 0
        Pixmap = 1
        Texture = 2

    def __init__(self, image_type=ImageType.Pixmap):
        if image_type == self.ImageType.Pixmap:
            self.requestPixmap = ffi.callback(
                'RequestPixmapCallback'
            )(self.requestPixmap)
            vptr = lib.dos_qquickimageprovider_create(
                self.requestPixmap
            )
        else:
            raise NotImplementedError
        self._vptr = ffi.gc(vptr, lib.dos_qquickimageprovider_delete)

    @staticmethod
    @abstractmethod
    def requestPixmap(id, width, height, req_width, req_height, result):
        """ do something like
        name = ptr2str(id)
        pixmap = QPixmap(result)
        pixmap.load(name)
        """
        raise NotImplementedError


class QQuickView(object):

    class SizeRootObjectToView(IntEnum):
        SizeViewToRootObject = 0
        SizeRootObjectToView = 1

    def __init__(self):
        vptr = lib.dos_qquickview_create()
        self._vptr = ffi.gc(vptr, lib.dos_qquickview_delete)

    @decode_cstring
    def source(self):
        return lib.dos_qquickview_source(self._vptr)

    def setSource(self, url):
        if not isinstance(url, QUrl):
            # lib.dos_qquickview_set_source(self._vptr, url)
            url = QUrl(url)
        lib.dos_qquickview_set_source_url(self._vptr, url._vptr)
    
    def show(self):
        lib.dos_qquickview_show(self._vptr)

    def setResizeMode(self, mode):
        lib.dos_qquickview_set_resize_mode(self._vptr, mode)

    def rootContext(self):
        return QQmlContext(lib.dos_qquickview_rootContext(self._vptr))
