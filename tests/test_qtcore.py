import pytest
from PyQuick.QtCore import (
    Signal,
    Slot,
    Property,
    QObject
)


def test_signal_slot_connection():
    class Foo(QObject):
        bar = Signal(int)

        def __init__(self):
            super(Foo, self).__init__()
            self.n = 0
            self.bar.connect(self.baz)
        
        @Slot(int)
        def baz(self, n):
            self.n = n
    
    
    foo = Foo()
    foo.bar.emit(3)
    assert foo.n == 3
