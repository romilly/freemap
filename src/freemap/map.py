from datetime import datetime
from typing import Optional

from html2text import html2text
from lxml import etree
from lxml.etree import tostring, Element

from freemap.helpers.base_map import minimal_map
from freemap.uuids import UUIDGenerator

MODIFIED = 'MODIFIED'

__author__ = 'romilly'


def datetime_from(timestamp_in_milliseconds: int) -> datetime:
    return datetime.fromtimestamp(float(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


def timestamp_in_millis(dt: datetime):
    return round(dt.timestamp()*1000)


def build_node_from(element: Element):
    if element.tag == 'node':
        return Branch(element)


def find_rich_content_in(xml, node_type):
    rc = xml.find('richcontent[@TYPE="%s"]' % node_type)
    if rc is not None:
        html = rc.find('html')
        text = etree.tostring(html)
        return html2text(text.decode('utf-8'))


def add_children_from_xml(xml_node, parent):
    for child_xml in xml_node:
        if child_xml.tag == 'node':
            new_branch = build_node_from(child_xml)
            child = parent.add_child(new_branch)
            add_children_from_xml(child_xml, child)
    return parent


def icons_in(node):
    return [Icons.icon(icon.get('BUILTIN')) for icon in node.findall('icon')]


def get_note_from(child_xml):
    rich_content = child_xml.find('richcontent')
    if rich_content is None:
        return None
    return etree.tostring(rich_content.find('html'), encoding=str)


class Icon():
    def __init__(self, name):
        self._name = name


class Icons(object):
    icon_dict = {}

    @classmethod
    def icon(cls, name):
        if name not in cls.icon_dict:
            cls.icon_dict[name] = Icon(name)
        return cls.icon_dict[name]


class Map:
    def __init__(self, root: Optional[Element] = None):
        if root is None:
            root = etree.XML(minimal_map)
        self._root = root
        root_node_xml = root.find('node')
        self.root_node = build_node_from(root_node_xml)
        add_children_from_xml(root_node_xml, self.root_node)

    def root(self) -> Element:
        return self.root_node

    def as_text(self) -> str:
        return tostring(self._root).decode('utf-8')

    @classmethod
    def from_string(cls, map_text: str):
        root = etree.XML(map_text)  # root is a map element
        return Map(root)


class Branch:
    def __init__(self, element: Optional[Element] = None):
        self._children = [] # the children will get added by the map if building a map
        if element is not None:
            self.element = element
        else:
            self.element = Element('node')
            self.node_id = UUIDGenerator.next_uuid()
            self.set('CREATED',(str(timestamp_in_millis(datetime.now()))))

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    def set_modified(self, ts):
        self.element.attributes[MODIFIED] = ts

    def created(self):
        return self.get('CREATED')

    def detail_markdown(self):
        return find_rich_content_in(self.element,'DETAILS')

    def modified(self):
        return self.get('MODIFIED')

    def localized_text(self):
        return self.get('LOCALIZED_TEXT')

    def text(self):
        return self.get('TEXT')

    def icons(self):
        return icons_in(self.element)

    def link(self):
        return self.get('LINK')

    def markdown_text(self) -> str:
        return find_rich_content_in(self.element,'NODE')

    def note(self):
        return get_note_from(self.element)

    def set_text(self, text):
        self.set('TEXT', text)

    def set_localized_text(self, text):
        self.set('LOCALIZED_TEXT', text)

    def set_link(self, link):
        self.set('LINK',link)

    def set_icons(self, icons):
        self.set('ICONS', icons if icons else [])

    def set(self, name, value):
        self.element.set(name,value)
        if name not in [MODIFIED, 'ID']:
            self.element.set(MODIFIED, str(timestamp_in_millis(datetime.now())))

    def get(self, name):
        if name in self.element.attrib:
            return self.element.get(name)
        return None

# TODO: these should create or update richtext children
    def set_note(self, note):
        self.set('NOTE', note if note else '')

    def set_markdown_text(self, text):
        self._attributes['MARKDOWN_TEXT'] = text

    def set_details_markdown(self, text):
        self._attributes['DETAILS_MARKDOWN'] = text
        pass

    def set_id(self, id_):
        self.set('ID', id_)

    def id(self):
        return self.get('ID')




