import html2text
import markdown as md
from lxml import etree
from lxml.etree import Element, SubElement

from freemap.map import NODE


class RichText:
    """represents the content of rich text nodes.

    Converts markdown to and from html"""
    def __init__(self):
        self._html = ''
        self._markdown = ''

    @property
    def markdown(self) -> str:
        return self._markdown

    @markdown.setter
    def markdown(self, markdown_text: str):
        self._markdown = markdown_text
        self._html = md.markdown(markdown_text)

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, html_text: str):
        self._html = html_text
        self._markdown = html2text.html2text(html_text).strip()

    def html_element(self, type: str) -> Element:
        rc = Element('richcontent')
        rc.attrib['TYPE'] = type
        html = SubElement(rc, 'html')
        SubElement(html, 'head')
        body = SubElement(html, 'body')
        body.append(etree.fromstring(self.html))
        return rc
