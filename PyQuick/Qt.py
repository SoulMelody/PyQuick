from enum import IntEnum


class ConnectionType(IntEnum):
    AutoConnection = 0
    DirectConnection = 1
    QueuedConnection = 2
    BlockingQueuedConnection = 3
    UniqueConnection = 0x80


class ItemDataRole(IntEnum):
    DisplayRole = 0
    DecorationRole = 1
    EditRole = 2
    ToolTipRole = 3
    StatusTipRole = 4
    WhatsThisRole = 5
    FontRole = 6
    TextAlignmentRole = 7
    BackgroundRole = 8
    ForegroundRole = 9
    CheckStateRole = 10
    AccessibleTextRole = 11
    AccessibleDescriptionRole = 12
    SizeHintRole = 13
    UserRole = 0x100
