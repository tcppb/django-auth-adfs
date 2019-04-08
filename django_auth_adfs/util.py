from django.utils.http import urlsafe_base64_encode

from django_auth_adfs.config import settings

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

def _decode_url(url):
    return urlsafe_base64_encode(url).decode()

try:
    import django
    if django.VERSION[0] > 1:
        def _decode_url(url):
            return urlsafe_base64_encode(url)
except:
    pass



def get_redirect_uri(hostname=None):
    if isinstance(settings.REDIR_URI, (list, tuple)):
        if hostname:
            for uri in settings.REDIR_URI:
                tmp_uri = uri if '://' in uri else 'x://%s' % uri
                parsed_uri = urlparse.urlparse(tmp_uri)
                if parsed_uri.netloc == hostname:
                    return uri
        return settings.REDIR_URI[0]

    return settings.REDIR_URI


def get_adfs_auth_url(next_url=None, hostname=None):
    """
    This function returns the ADFS authorization URL.

    Returns:
        str: The redirect URI

    """
    url = "https://{0}{1}?response_type=code&client_id={2}&resource={3}&redirect_uri={4}".format(
        settings.SERVER,
        settings.AUTHORIZE_PATH,
        settings.CLIENT_ID,
        settings.RESOURCE,
        get_redirect_uri(hostname),
    )
    if next_url:
        url += "&state={0}".format(_decode_url(next_url.encode()))
    return url
