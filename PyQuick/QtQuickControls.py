from PyQuick.DOtherSide import lib
from PyQuick.utils import encode_first_arg


class QQuickStyle(object):
    
    @encode_first_arg
    @staticmethod
    def setStyle(style):
        lib.dos_qquickstyle_set_style(style)

    @encode_first_arg
    @staticmethod
    def setFallbackStyle(style):
        lib.dos_qquickstyle_set_fallback_style(style)
