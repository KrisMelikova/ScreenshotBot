import re


def match_url(string):
    # Just check if it's a valid http(s) URL to minimally secure our headless browser
    regex = r'^http[s]{0,1}:\/\/(.*)'
    url = re.fullmatch(regex, string)
    # User can give us a link without scheme
    url_w_added_protocol = f'http://{string}'

    return url.string if url else url_w_added_protocol
