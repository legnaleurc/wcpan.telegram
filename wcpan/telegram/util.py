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


def generate_multipart_formdata(fields):
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'

    async def stream(write):
        for (key, value) in fields:
            if not isinstance(value, types.InputFile):
                await _crlf_bytes(write, '--' + BOUNDARY)
                await _crlf_bytes(write, 'Content-Disposition: form-data; name="%s"' % key)
                await _crlf_bytes(write, '')
                await _crlf_bytes(write, value)
            else:
                await _crlf_bytes(write, '--' + BOUNDARY)
                await _crlf_bytes(write, 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, value.name))
                await _crlf_bytes(write, 'Content-Type: %s' % value.content_type)
                await _crlf_bytes(write, 'Content-Length: %s' % value.size)
                await _crlf_bytes(write, '')
                for chunk in value.stream():
                    await write(chunk)
                await _crlf_bytes(write, '')
        await _crlf_bytes(write, '--' + BOUNDARY + '--')

    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

    return content_type, stream


def normalize_args(args):
    PrimitiveTypes = (bool, int, float, str, list, dict, types.InputFile)
    new_args = ((k, v if isinstance(v, PrimitiveTypes) else str(v)) for k, v in args.items())
    return dict(new_args)


def _append_bytes(l, value):
    l.append(_to_bytes(value))


async def _crlf_bytes(write, value):
    b = _to_bytes(value) + '\r\n'.encode('utf-8')
    await write(b)


def _to_bytes(value):
    if isinstance(value, str):
        return value.encode('utf-8')
    elif isinstance(value, (int, float)):
        return str(value).encode('utf-8')
    elif isinstance(value, bool):
        return ('true' if value else 'false').encode('utf-8')
    else:
        return value
