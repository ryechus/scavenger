import requests


async def get_content(url):
    """Downloads contents of media at provided URL.

    :param url: URL of the media field to download
    :type: str

    :raises: DownloadError

    :returns: file-like object
    :rtype: file
    """
    response = requests.get(url)

    return response
