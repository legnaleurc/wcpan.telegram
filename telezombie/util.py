from tornado import gen

from . import types


def encode_multipart_formdata(fields):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'.encode('utf-8')
    L = []
    for (key, value) in fields:
        if not isinstance(value, types.InputFile):
            _append_bytes(L, '--' + BOUNDARY)
            _append_bytes(L, 'Content-Disposition: form-data; name="%s"' % key)
            _append_bytes(L, '')
            _append_bytes(L, value)
        else:
            _append_bytes(L, '--' + BOUNDARY)
            _append_bytes(L, 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value.name))
            _append_bytes(L, 'Content-Type: %s' % value.content_type)
            _append_bytes(L, '')
            _append_bytes(L, value.content)
    _append_bytes(L, '--' + BOUNDARY + '--')
    _append_bytes(L, '')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def encode_multipart_formdata_2(fields):
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'

    @gen.coroutine
    def stream(write):
        for (key, value) in fields:
            if not isinstance(value, types.InputFile):
                yield _crlf_bytes(write, '--' + BOUNDARY)
                yield _crlf_bytes(write, 'Content-Disposition: form-data; name="%s"' % key)
                yield _crlf_bytes(write, '')
                yield _crlf_bytes(write, value)
            else:
                yield _crlf_bytes(write, '--' + BOUNDARY)
                yield _crlf_bytes(write, 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value.name))
                yield _crlf_bytes(write, 'Content-Type: %s' % value.content_type)
                yield _crlf_bytes(write, 'Content-Length: %s' % value.size)
                yield _crlf_bytes(write, '')
                for chunk in value.stream():
                    yield write(chunk)
                yield _crlf_bytes(write, '')
        yield _crlf_bytes(write, '--' + BOUNDARY + '--')

    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

    return content_type, stream


def _append_bytes(l, value):
    l.append(_to_bytes(value))


@gen.coroutine
def _crlf_bytes(write, value):
    b = _to_bytes(value) + '\r\n'.encode('utf-8')
    yield write(b)


def _to_bytes(value):
    if isinstance(value, str):
        return value.encode('utf-8')
    elif isinstance(value, (int, float)):
        return str(value).encode('utf-8')
    elif isinstance(value, bool):
        return ('true' if value else 'false').encode('utf-8')
    else:
        return value
