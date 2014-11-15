from urlparse import urlparse, parse_qs

def clean_message_from_url(url):
    """
    strip message parameter from url
    :param url:
    :return: string
    """
    if not url:
        return None

    o = urlparse(url)

    if not o.query:
        return url

    query_string = ''

    for key, value in parse_qs(o.query).iteritems():
        if key != 'message':
            query_string = '%s%s=%s&' % (query_string, key, value[0],)

    url = '%s://%s%s' % (o.scheme, o.netloc, o.path,)

    if query_string:
        url = '%s?%s' % (url, query_string.strip('&'),)

    return url