def encode_multipart_formdata(fields):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        if isinstance(value, str):
            _append_bytes(L, '--' + BOUNDARY)
            _append_bytes(L, 'Content-Disposition: form-data; name="%s"' % key)
            _append_bytes(L, '')
            _append_bytes(L, value)
        else:
            filename = value.name.encode('utf-8')
            _append_bytes(L, '--' + BOUNDARY)
            _append_bytes(L, 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            _append_bytes(L, 'Content-Type: %s' % value.content_type)
            _append_bytes(L, '')
            _append_bytes(L, value.content)
    _append_bytes(L, '--' + BOUNDARY + '--')
    _append_bytes(L, '')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def _append_bytes(l, sb):
    if isinstance(sb, str):
        b = sb.encode('utf-8')
    else:
        b = sb
    l.append(b)
