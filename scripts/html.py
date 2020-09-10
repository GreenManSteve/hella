import re


def clean_html(raw_html):
    clean_compile = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    clean_text = re.sub(clean_compile, '', raw_html)
    return clean_text