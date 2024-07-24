from xml.etree import ElementTree

import requests

SUFFIX = "</head>"


def read(url: str) -> tuple[str, str, str]:
    content = requests.get(url)
    xml = ElementTree.fromstring(convert_to_html_snippet(content.text))

    title = xml.find("meta[@property=\"og:title\"]").get("content")
    image_url = xml.find("meta[@property=\"og:image\"]").get("content")
    description = xml.find("meta[@property=\"og:description\"]").get("content")
    return title, image_url, description


def convert_to_html_snippet(raw_html):
    start = raw_html.index("<head>")
    end = raw_html.index("<meta name=\"twitter:site\"")
    html_snippet = raw_html[start:end] + SUFFIX
    return html_snippet
