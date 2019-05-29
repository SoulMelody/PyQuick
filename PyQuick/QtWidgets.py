from PyQuick.DOtherSide import lib
from PyQuick.QtGui import QGuiApplication


class QApplication(QGuiApplication):
    def __init__(self, argv=None):
        lib.dos_qapplication_create()

    def __del__(self):
        lib.dos_qapplication_delete()

    def exec_(self):
        lib.dos_qapplication_exec()
    
    def quit(self):
        lib.dos_qapplication_quit()


qApp = QApplication
