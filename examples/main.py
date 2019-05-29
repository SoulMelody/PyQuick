# coding: utf-8
from PyQuick.QtCore import QVariant, QResource, QObject, Property, Slot, Signal, Property
from PyQuick.QtGui import QPixmap
from PyQuick.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQuick.QtQuick import QQuickView, QQuickImageProvider
from PyQuick.QtWidgets import QApplication
from PyQuick.QtQuickControls import QQuickStyle


class Calculator(QObject):
    outChanged = Signal(float)

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self._out = 0.0

    @Slot(result=float)
    def out(self):
        return self._out

    getOut = Property(float, notify=outChanged)(out)

    @Slot(float, float)
    def _calculate(self, _in1, _in2):
        self._out = _in1 + _in2
        self.outChanged.emit(self._out)


if __name__ == '__main__':
    app = QApplication()
    qmlRegisterType(Calculator, 'example.module', 1, 0, Calculator.__name__)
    QQuickStyle.setStyle('Material')
    QResource.registerResource('res.rcc')
    engine = QQmlApplicationEngine()
    qVar1 = QVariant(10)
    qVar2 = QVariant("你好世界")
    qVar3 = QVariant(False)
    qVar4 = QVariant(3.5)
    context = engine.rootContext()
    context.setContextProperty("qVar1", qVar1)
    context.setContextProperty("qVar2", qVar2)
    context.setContextProperty("qVar3", qVar3)
    context.setContextProperty("qVar4", qVar4)
    engine.load('examples/main.qml')
    app.exec_()
