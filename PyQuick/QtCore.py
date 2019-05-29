from __future__ import unicode_literals

import functools
from abc import ABCMeta
from enum import IntEnum

from six import (add_metaclass, ensure_binary, ensure_text, string_types,
                 text_type)

from PyQuick import Qt
from PyQuick.DOtherSide import ffi, lib
from PyQuick.utils import encode_first_arg, decode_cstring, ptr2str, str2ptr


__all__ = [
    'QObject',
    'Slot',
    'Signal',
    'Property',
    'QCoreApplication',
    'QMetaType',
    'QMetaObject',
    'QVariant',
    'QResource',
    'QModelIndex',
    'QUrl',
    'Qt',
    'QAbstractItemModel',
    'QAbstractListModel',
    'QAbstractTableModel',
]


MAX_INT = 2 ** 31 - 1
MIN_INT = -MAX_INT - 1


TYPE_MAP = {
    'bool': 'bool',
    'int': 'int',
    'float': 'double',
    'str': 'QString',
    'QVariant': 'QVariant',
    'list': 'QVariantList',
    'NoneType': 'Void'
}


def check_type(arg):
    if isinstance(arg, type):
        arg = TYPE_MAP.get(arg.__name__, arg)
    if isinstance(arg, string_types):
        arg = ensure_text(arg)
        metaType = QMetaType.type(arg)
        if metaType != QMetaType.Type.UnknownType:
            return metaType
        else:
            raise TypeError('C type {0!r} is not supported as a Signal() type argument type'.format(arg))
    else:
        raise TypeError('bytes or ASCII string expected not {0!r}'.format(type(arg).__name__))


@add_metaclass(ABCMeta)
class Connector(object):
    @property
    def signatures(self):
        return '{}({})'.format(
            self.name,
            ','.join(QMetaType.typeName(arg) for arg in self.argtypes)
        )


class Slot(Connector):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', '')
        self.result = check_type(kwargs.get('result', 'void'))
        self.argtypes = tuple(
            check_type(arg) for arg in args
        )
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if name.startswith('get'):
            name = name[3].lower() + name[4:]
        self._name = name

    @property
    def signatures(self):
        return '{}({})'.format(
            self.name,
            ','.join(QMetaType.typeName(arg) for arg in self.argtypes)
        )

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(obj, *args, **kwargs):
            return func(obj, *args, **kwargs)
        wrapper._slot = self
        return wrapper


class Signal(Connector):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', '')
        self.argtypes = tuple(check_type(arg) for arg in args)

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return BoundSignal(obj, self)


class BoundSignal(object):
    def __init__(self, obj, signal):
        self.obj = obj
        self.signal = signal

    def emit(self, *args):
        argv = tuple(QVariant(arg)._vptr for arg in args)
        lib.dos_qobject_signal_emit(
            self.obj._vptr,
            str2ptr(self.signal.name),
            len(args),
            ffi.new(
                'DosQVariant* []',
                argv
            ) if len(args) else ffi.NULL
        )

    def connect(self, slot, **kwargs):
        connection_type = kwargs.get('type', Qt.ConnectionType.AutoConnection)
        # no_receiver_check = kwargs.get('no_receiver_check', False)
        result = lib.dos_qobject_signal_connect(
            self.obj._vptr,
            str2ptr('2' + self.signal.signatures),
            self.obj._vptr,
            str2ptr('1' + slot._slot.signatures),
            connection_type
        )
        return result

    def disconnect(self, slot):
        return lib.dos_qobject_signal_disconnect(
            self.obj._vptr,
            str2ptr('2' + self.signal.signatures),
            self.obj._vptr,
            str2ptr('1' + slot._slot.signatures),
        )


class PropertyInstance(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, notify=None, type_=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if fget is not None:
            if doc is None:
                doc = fget.__doc__
        self.__doc__ = doc
        self.notify = notify
        self.type = type_
        self.name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = ensure_binary(name)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        lib.dos_qobject_property(obj._vptr, self.name)
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        lib.dos_qobject_setProperty(obj._vptr, self.name, QVariant(value)._vptr)
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__, self.notify, type_=self.type)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__, self.notify, type_=self.type)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__, self.notify, type_=self.type)


class Property:
    def __init__(self, type_, notify=None):
        self.type = check_type(type_)
        self.notify = notify

    def __call__(self, fget, fset=None, fdel=None, doc=''):
        return PropertyInstance(fget, fset, fdel, doc, notify=self.notify, type_=self.type)


class QMetaType(object):

    class Type(IntEnum):
        Bool = 1
        Int = 2
        Double = 6
        List = 9
        QString = 10
        VoidStar = 31
        QObjectStar = 39
        QVariant = 41
        Void = 43
        User = 1024
        UnknownType = 0

    @classmethod
    def type(cls, type_):
        if type_ == 'int':
            return cls.Type.Int
        elif type_ == 'bool':
            return cls.Type.Bool
        elif type_ in 'double':
            return cls.Type.Double
        elif type_ in 'QString':
            return cls.Type.QString
        elif type_ == 'QObject*':
            return cls.Type.QObjectStar
        elif type_ == 'QVariant':
            return cls.Type.QVariant
        elif type_ == 'QVariantList':
            return cls.Type.List
        elif type_ == 'void':
            return cls.Type.Void
        elif type_ == 'void *':
            return cls.Type.VoidStar
        else:
            return cls.Type.UnknownType

    @classmethod
    def typeName(cls, type_):
        if type_ == cls.Type.Bool:
            return 'bool'
        elif type_ == cls.Type.Int:
            return 'int'
        elif type_ == cls.Type.Double:
            return 'double'
        elif type_ == cls.Type.QString:
            return 'QString'
        elif type_ == cls.Type.QObjectStar:
            return 'QObject*'
        elif type_ == cls.Type.QVariant:
            return 'QVariant'
        elif type_ == cls.Type.List:
            return 'QVariantList'
        elif type_ == cls.Type.Void:
            return 'void'
        elif type_ == cls.Type.VoidStar:
            return 'void *'
        else:
            return ''


class QMetaObject(object):
    def __init__(self, vptr=None):
        self._vptr = ffi.gc(vptr, lib.dos_qmetaobject_delete)

    @classmethod
    def new(cls, superClass, className, signalDefinitions, slotDefinitions, propertyDefinitions):
        return cls(
            lib.dos_qmetaobject_create(
                superClass._vptr,
                str2ptr(className),
                signalDefinitions,
                slotDefinitions,
                propertyDefinitions
            )
        )


class QObjectMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if '_metaObject' not in attrs:
            signals = []
            slots = []
            properties = []
            for k, v in attrs.items():
                if isinstance(v, Signal):
                    if len(v.name) == 0:
                        v.name = k
                    param_defs = ffi.new(
                        'ParameterDefinition []',
                        tuple(
                            {
                                'name': str2ptr('arg%d' % i),
                                'metaType': sig
                            }
                            for i, sig in enumerate(v.argtypes)
                        )
                    ) if len(v.argtypes) else ffi.NULL
                    signals.append({
                        'name': str2ptr(v.name),
                        'parametersCount': len(v.argtypes),
                        'parameters': param_defs
                    })
                elif hasattr(v, '_slot'):
                    v = v._slot
                    if len(v.name) == 0:
                        v.name = k
                    param_defs = ffi.new(
                        'ParameterDefinition []',
                        tuple(
                            {
                                'name': str2ptr('arg%d' % i),
                                'metaType': sig
                            }
                            for i, sig in enumerate(v.argtypes)
                        )
                    ) if len(v.argtypes) else ffi.NULL
                    slots.append({
                        'name': str2ptr(v.name),
                        'returnMetaType': v.result,
                        'parametersCount': len(v.argtypes),
                        'parameters': param_defs
                    })
                elif isinstance(v, PropertyInstance):
                    if len(v.name) == 0:
                        v.name = k
                    properties.append({
                        'name': str2ptr(v.name),
                        'propertyMetaType': v.type,
                        'readSlot': str2ptr('' if v.fget is None else v.fget._slot.name),
                        'writeSlot': str2ptr('' if v.fset is None else v.fset._slot.name),
                        'notifySignal': str2ptr(getattr(v.notify, 'name', '')),
                    })
            signal_defs = ffi.new(
                'const SignalDefinitions *',
                {
                    'count': len(signals),
                    'definitions': ffi.new(
                        'SignalDefinition []',
                        signals
                    )
                }
            )
            slot_defs = ffi.new(
                'const SlotDefinitions *',
                {
                    'count': len(slots),
                    'definitions': ffi.new(
                        'SlotDefinition []',
                        slots
                    )
                }
            )
            property_defs = ffi.new(
                'const PropertyDefinitions *',
                {
                    'count': len(properties),
                    'definitions': ffi.new(
                        'PropertyDefinition []',
                        properties
                    )
                }
            )
            attrs['_metaObject'] = QMetaObject.new(
                bases[0]._metaObject,
                name,
                signal_defs,
                slot_defs,
                property_defs
            )
        return type.__new__(cls, name, bases, attrs)


@add_metaclass(QObjectMetaclass)
class QObject(object):
    _metaObject = QMetaObject(lib.dos_qobject_qmetaobject())

    def __init__(self, parent=None):
        self.slot_callback = ffi.callback('DObjectCallback')(
            self.slot_callback
        )
        self._handle = ffi.new_handle(self)
        ptr = lib.dos_qobject_create(
            self._handle,
            self.metaObject()._vptr,
            self.slot_callback
        )
        self._vptr = ffi.gc(ptr, lib.dos_qobject_delete)

    @staticmethod
    def slot_callback(qobject_ptr, slot_name_ptr, parameters_count, parameters):
        qobject = ffi.from_handle(qobject_ptr)
        slot_name = QVariant(slot_name_ptr).toString()
        params = tuple(QVariant(param)
                  for param in ffi.unpack(parameters, parameters_count)[1:])
        try:
            func_sigs = getattr(qobject, slot_name)._slot.argtypes
        except AttributeError:
            slot_name = 'get' + slot_name[0].upper() + slot_name[1:]
            func_sigs = getattr(qobject, slot_name)._slot.argtypes
        for param, sig in zip(params, func_sigs):
            param._type = sig
        params = (param.value() for param in params)
        result = QVariant(qobject._on_slot_called(slot_name, params))
        if result is not None:
            lib.dos_qvariant_assign(parameters[0], result._vptr)

    def deleteLater(self):
        lib.dos_qobject_deleteLater(self._vptr)

    def _on_slot_called(self, slot_name, arguments):
        return getattr(self, slot_name)(*arguments)

    @property
    def staticMetaObject(self):
        return self._metaObject

    @classmethod
    def metaObject(cls):
        return cls._metaObject
    
    @decode_cstring
    def objectName(self):
        return lib.dos_qobject_objectName(self._vptr)
    
    @encode_first_arg
    def setObjectName(self, name):
        lib.dos_qobject_setObjectName(self._vptr, name)

    @encode_first_arg
    def property(self, name):
        return getattr(self, name)

    @encode_first_arg
    def setProperty(self, name, value):
        return setattr(self, name, value)
    

class QVariant(object):
    _BASE_TYPES = {
        QMetaType.Type.Int,
        QMetaType.Type.Bool,
        QMetaType.Type.Double,
        QMetaType.Type.QString,
        QMetaType.Type.QVariant
    }

    def __init__(self, val=None):
        if isinstance(val, bool):
            vptr = lib.dos_qvariant_create_bool(val)
            self._type = QMetaType.Type.Bool
        elif isinstance(val, int) and MIN_INT <= val <= MAX_INT:
            vptr = lib.dos_qvariant_create_int(val)
            self._type = QMetaType.Type.Int
        elif isinstance(val, string_types):
            vptr = lib.dos_qvariant_create_string(str2ptr(val))
            self._type = QMetaType.Type.QString
        elif isinstance(val, QVariant):
            self._value = val._vptr
            vptr = lib.dos_qvariant_create_qvariant(val._vptr)
            self._type = QMetaType.Type.QVariant
        elif isinstance(val, ffi.CData) and ffi.typeof(val).cname == 'void *':
            vptr = lib.dos_qvariant_create_qvariant(val)
            self._type = QMetaType.Type.QVariant
        elif isinstance(val, QObject):
            vptr = lib.dos_qvariant_create_qobject(val._vptr)
            self._type = QMetaType.Type.QObjectStar
        elif isinstance(val, float):
            vptr = lib.dos_qvariant_create_double(val)
            self._type = QMetaType.Type.Double
        elif val is None:
            vptr = lib.dos_qvariant_create()
            self._type = QMetaType.Type.UnknownType
        else:
            raise NotImplementedError()
        if isinstance(val, ffi.CData) and ffi.typeof(val).cname == 'void *':
            self._vptr = vptr
        else:
            self._vptr = ffi.gc(vptr, lib.dos_qvariant_delete)

    def __int__(self):
        return lib.dos_qvariant_toInt(self._vptr)

    def __float__(self):
        return lib.dos_qvariant_toDouble(self._vptr)
    
    def __bool__(self):
        return lib.dos_qvariant_toBool(self._vptr)

    @decode_cstring
    def toString(self):
        return lib.dos_qvariant_toString(self._vptr)
    
    def isNull(self):
        return lib.dos_qvariant_isnull(self._vptr)

    def canConvert(self, type_):
        if type_ in self._BASE_TYPES and self._type in self._BASE_TYPES:
            return True
        elif type_ == self._type:
            return True
        else:
            return False
    
    def convert(self, type_):
        if self.canConvert(type_):
            if type_ == QMetaType.Type.Int:
                val = int(self)
            elif type_ == QMetaType.Type.Bool:
                val = bool(self)
            elif type_ == QMetaType.Type.Double:
                val = float(self)
            elif type_ == QMetaType.Type.QString:
                val = self.toString()
            elif type_ == QMetaType.Type.QVariant:
                val = QVariant(self)
            else:
                raise NotImplementedError()
            if type_ != self._type:
                self.setValue(val)
            return True
        else:
            return False
    
    def type(self):
        return self._type
    
    userType = type
    
    def typeName(self):
        return self.typeToName(self._type)
    
    @staticmethod
    def typeToName(type_):
        return QMetaType.typeName(type_)

    @staticmethod
    def nameToType(name):
        return QMetaType.type(name)

    def clear(self):
        self.setValue(None)

    def value(self):
        if self._type == QMetaType.Type.Int:
            val = int(self)
        elif self._type == QMetaType.Type.Bool:
            val = bool(self)
        elif self._type == QMetaType.Type.Double:
            val = float(self)
        elif self._type == QMetaType.Type.QString:
            val = self.toString()
        elif self._type == QMetaType.Type.QVariant:
            val = QVariant(self)
        elif self._type == QMetaType.Type.UnknownType:
            val = None
        else:
            raise NotImplementedError()
        return val

    def setValue(self, val):
        if isinstance(val, bool):
            lib.dos_qvariant_setBool(self._vptr, val)
            self._type = QMetaType.Type.Bool
        elif isinstance(val, int) and MIN_INT <= val <= MAX_INT:
            lib.dos_qvariant_setInt(self._vptr, val)
            self._type = QMetaType.Type.Int
        elif isinstance(val, string_types):
            lib.dos_qvariant_setString(self._vptr, str2ptr(val))
            self._type = QMetaType.Type.QString
        elif isinstance(val, QVariant):
            self._value = val._vptr
            lib.dos_qvariant_assign(self._vptr, val._vptr)
            self._type = QMetaType.Type.QVariant
        elif isinstance(val, ffi.CData) and ffi.typeof(val).cname == 'void *':
            self._vptr = val
            self._type = QMetaType.Type.QVariant
        elif isinstance(val, QObject):
            lib.dos_qvariant_setQobject(self._vptr, val._vptr)
            self._type = QMetaType.Type.QObjectStar
        elif isinstance(val, float):
            lib.dos_qvariant_setDouble(self._vptr, val)
            self._type = QMetaType.Type.Double
        elif val is None:
            self._type = QMetaType.Type.UnknownType
        else:
            raise NotImplementedError()


class QAbstractItemModel(QObject):
    _metaObject = QMetaObject(lib.dos_qabstractitemmodel_qmetaobject())

    # TODO


class QAbstractListModel(QAbstractItemModel):
    _metaObject = QMetaObject(lib.dos_qabstractlistmodel_qmetaobject())

    # TODO

class QAbstractTableModel(QAbstractItemModel):
    _metaObject = QMetaObject(lib.dos_qabstracttablemodel_qmetaobject())

    # TODO

class QResource(object):
    @encode_first_arg
    @staticmethod
    def registerResource(filename):
        lib.dos_qresource_register(filename)


class QUrl(object):
    
    class ParsingMode(IntEnum):
        TolerantMode = 0
        StrictMode = 1
        DecodedMode = 2


    @encode_first_arg
    def __init__(self, url, mode=ParsingMode.TolerantMode):
        vptr = lib.dos_qurl_create(url, mode)
        self._vptr = ffi.gc(vptr, lib.dos_qurl_delete)
    
    @decode_cstring
    def toString(self):
        return lib.dos_qurl_to_string(self._vptr)
    
    def isValid(self):
        return lib.dos_qurl_isValid(self._vptr)


class QModelIndex(object):
    def __init__(self, other):
        if other is None:
            vptr = lib.dos_qmodelindex_create()
        else:
            vptr = other
        self._vptr = ffi.gc(vptr, lib.dos_qmodelindex_delete)

    def data(self, role=Qt.ItemDataRole.DisplayRole):
        return QVariant(lib.dos_qmodelindex_data(self._vptr, role))
    
    def row(self):
        return lib.dos_qmodelindex_row(self._vptr)
    
    def column(self):
        return lib.dos_qmodelindex_column(self._vptr)
    
    def isValid(self):
        return lib.dos_qmodelindex_isValid(self._vptr)
    
    def internalPointer(self):
        return lib.dos_qmodelindex_internalPointer(self._vptr)
    
    def parent(self):
        return QModelIndex(lib.dos_qmodelindex_parent(self._vptr))

    def child(self, row, column):
        return QModelIndex(lib.dos_qmodelindex_child(self._vptr, row, column))
    
    def sibling(self, row, column):
        return QModelIndex(lib.dos_qmodelindex_sibling(self._vptr, row, column))


class QHashIntByteArray(object):

    def __init__(self):
        vptr = lib.dos_qhash_int_qbytearray_create()
        self._vptr = ffi.gc(vptr, lib.dos_qhash_int_qbytearray_delete)
    
    @decode_cstring
    def __getitem__(self, key):
        return lib.dos_qhash_int_qbytearray_value(self._vptr, key)
    
    def __setitem__(self, key, value):
        value = ensure_binary(value)
        lib.dos_qhash_int_qbytearray_insert(self._vptr, key, value)


@add_metaclass(ABCMeta)
class QCoreApplication(object):
    @decode_cstring
    def applicationDirPath(self):
        return lib.dos_qcoreapplication_application_dir_path()
