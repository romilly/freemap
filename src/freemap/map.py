from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from lxml import etree
from lxml.etree import tostring, Element

from freemap.helpers.base_map import minimal_map
from freemap.rich_text import RichText
from freemap.uuids import UUIDGenerator

LOCALIZED_TEXT = 'LOCALIZED_TEXT'
MODIFIED = 'MODIFIED'
NODE = 'NODE'
TEXT = 'TEXT'

__author__ = 'romilly'


def datetime_from(timestamp_in_milliseconds: int) -> datetime:
    return datetime.fromtimestamp(float(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


def timestamp_in_millis(dt: datetime):
    return round(dt.timestamp()*1000)


def build_node_from(element: Element):
    if element.tag == 'node':
        return Branch(element)


def find_rich_content_in(xml, node_type) -> Optional[RichText]:
    rc = xml.find('richcontent[@TYPE="%s"]' % node_type)
    if rc is None:
        return None
    html = rc.find('html')
    text = etree.tostring(html)
    rt = RichText()
    rt.html = text.decode('utf-8')
    return rt


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


class Icon:
    def __init__(self, name):
        self._name = name


class Icons(object):
    icon_dict = {}

    @classmethod
    def icon(cls, name):
        if name not in cls.icon_dict:
            cls.icon_dict[name] = Icon(name)
        return cls.icon_dict[name]

@abstractmethod
class MapElement(ABC):
    def __init__(self, element: Optional[Element] = None):
        if element is not None:
            self.element = element
        else:
            self.set_default_element()

    @abstractmethod
    def set_default_element(self):
        pass

    @classmethod
    def from_string(cls, map_text: str):
        element = etree.XML(map_text)  # root is a map element
        return cls(element)

    def as_text(self) -> str:
        return tostring(self.element).decode('utf-8')


class Map(MapElement):
    def __init__(self, element: Optional[Element] = None):
        MapElement.__init__(self, element)
        root_node_xml = self.element.find('node')
        self.root_node = build_node_from(root_node_xml)
        add_children_from_xml(root_node_xml, self.root_node)

    def set_default_element(self):
        self.element = etree.XML(minimal_map)

    def root(self) -> Element:
        return self.root_node


class Branch(MapElement):
    def __init__(self, element: Optional[Element] = None):
        MapElement.__init__(self, element)
        self._children = [] # the children will get added by the map if building a map

    def set_default_element(self):
        self.element = Element('node')
        self.set('ID', str(UUIDGenerator.next_uuid()))
        self.set('CREATED', (str(timestamp_in_millis(datetime.now()))))

    def add_child(self, branch):
        self._children.append(branch)
        # TODO: add a test, then add self._update_modified()
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    @property
    def modified(self) -> int:
        """The timestamp (in ms) when this branch was last modified.

        There is no setter, as the value is changed only by changing some other property
        """
        return int(self.get('MODIFIED'))

    @property
    def created(self) -> int:
        """ The timestamp (in ms) when this branch was created."""
        # no setter, as the value is only set (indirectly) in the constructor.
        return int(self.get('CREATED'))

    @property
    def details(self) -> RichText:
        """The details of a node"""
        return find_rich_content_in(self.element,'DETAILS')

    # def localized_text(self):

    @property
    def text(self):
        """the text attribute of a node.

        Returns the value of LOCALIZED_TEXT or TEXT as a string,
        or the contents of the relevant RICH_TEXT node as Markdown
        """
        if LOCALIZED_TEXT in self.element.attrib:
            return self.get(LOCALIZED_TEXT)
        if TEXT in self.element.attrib:
            return self.get(TEXT)
        return find_rich_content_in(self.element, NODE)

    def icons(self):
        return icons_in(self.element)

    @property
    def link(self) -> str:
        """returns the hyperlink of a node."""
        return self.get('LINK')

    @link.setter
    def link(self, value: str):
        self.set('LINK', value)

    @property
    def note(self) -> RichText:
        """the note attached to a node

        :return: rich text from note
        """
        return find_rich_content_in(self.element,'NOTE')

    def set_text(self, text):
        self.set('TEXT', text)

    def set_link(self, link):
        self.set('LINK',link)

    def set_icons(self, icons):
        self.set('ICONS', icons if icons else [])

    def set(self, name, value):
        self.element.set(name,value)
        if name not in [MODIFIED, 'ID']:
            self._update_modified()

    def _update_modified(self):
        self.element.set(MODIFIED, str(timestamp_in_millis(datetime.now())))

    @property
    def node_id(self) -> Optional[str]:
        return self.get('ID')

    def get(self, name) -> Optional[str]:
        if name in self.element.attrib:
            return self.element.get(name)
        return None




