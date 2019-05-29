import wrapt
from six import ensure_binary, ensure_text, text_type

from PyQuick.DOtherSide import ffi, lib


@wrapt.decorator
def encode_first_arg(wrapped, instance, args, kwargs):
    if len(args) and isinstance(args[0], text_type):
        return wrapped(ensure_binary(args[0]), *args[1:], **kwargs)
    return wrapped(*args, **kwargs)


@wrapt.decorator
def decode_cstring(wrapped, instance, args, kwargs):
    cstr = wrapped(*args, **kwargs)
    cstr = ffi.gc(cstr, lib.dos_chararray_delete)
    return ptr2str(cstr)


def ptr2str(cstr):
    return ensure_text(ffi.string(cstr))


def str2ptr(text):
    encoded = ensure_binary(text)
    return ffi.new('const char []', encoded)
