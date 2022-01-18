from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from lxml import etree
from lxml.etree import tostring, Element, SubElement

from freemap.attributes import *
from freemap.helpers.base_map import minimal_map
from freemap.rich_text import RichText
from freemap.uuids import UUIDGenerator


__author__ = 'romilly'


def datetime_from(timestamp_in_milliseconds: int) -> datetime:
    return datetime.fromtimestamp(float(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


def timestamp_in_millis(dt: datetime):
    return round(dt.timestamp()*1000)


def build_node_from(element: Element):
    if element.tag == 'node':
        return Branch(element)


def add_children_from_xml(xml_node, parent):
    for child_xml in xml_node:
        if child_xml.tag == 'node':
            new_branch = build_node_from(child_xml)
            child = parent.add_child(new_branch)
            add_children_from_xml(child_xml, child)
    return parent


def icons_in(node):
    return [Icons.icon(icon.get(BUILTIN)) for icon in node.findall('icon')]


class Icon:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


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

    def get(self, name) -> Optional[str]:
        if name in self.element.attrib:
            return self.element.get(name)
        return None

    def set(self, name, value):
        self.element.set(name,value)


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

    def branch_with_id(self, node_id):
        # horrible but it works
        for branch in self.all_branches():
            if branch.node_id == node_id:
                return branch

    def all_branches(self):
        return self.root().all_branches()


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

    def find_rich_content_for(self, node_type) -> Optional[RichText]:
        rc = self.find_rich_content_element(node_type)
        if rc is None:
            return None
        html = rc.find('html')
        text = etree.tostring(html)
        rt = RichText()
        rt.html = text.decode('utf-8')
        return rt

    def find_rich_content_element(self, node_type):
        rc = self.element.find('richcontent[@TYPE="%s"]' % node_type)
        return rc

    def has_rich_content(self) -> bool:
        return self.find_rich_content_for('NODE') is not None

    @property
    def modified(self) -> int:
        """The timestamp (in ms) when this branch was last modified.

        There is no setter, as the value is changed only by changing some other property
        """
        return int(self.get(MODIFIED))

    @property
    def created(self) -> int:
        """ The timestamp (in ms) when this branch was created."""
        # no setter, as the value is only set (indirectly) in the constructor.
        return int(self.get(CREATED))

    @property
    def details(self) -> RichText:
        """The details of a node"""
        return self.find_rich_content_for(DETAILS)

    @details.setter
    def details(self, new_content):
        self.remove_rich_content(DETAILS)
        self.add_rich_content(new_content, DETAILS)


    # def localized_text(self):

    def _get_text(self):
        result = None
        if LOCALIZED_TEXT in self.element.attrib:
            result = self.get(LOCALIZED_TEXT)
        elif TEXT in self.element.attrib:
            result = self.get(TEXT)
        return result


    @property
    def text(self) -> str:
        """the text attribute of a node.

        Returns the value of LOCALIZED_TEXT, TEXT or richcontent as a markdown string.
        """
        result = self._get_text()
        if result is None:
            result = self.find_rich_content_for(NODE).markdown
        return result

    @text.setter
    def text(self, localized_text: str):
        if TEXT in self.element.attrib:
            del self.element.attrib[TEXT]
        if self.has_rich_content():
            rc = self.element.find('richcontent[@TYPE="NODE"]')
            self.element.remove(rc)
        self.set(LOCALIZED_TEXT, localized_text)

    @property
    def rich_content(self) -> RichText:
        result = self._get_text()
        if result is None:
            result = self.find_rich_content_for(NODE)
        else:
            rt = RichText()
            rt.markdown = result
            result = rt
        return result

    @rich_content.setter
    def rich_content(self, new_content: str):
        result = self._get_text()
        if result is not None:
            if TEXT in self.element.attrib:
                del self.element.attrib[TEXT]
            if LOCALIZED_TEXT in self.element.attrib:
                del self.element.attrib[LOCALIZED_TEXT]
        else:
            self.remove_rich_content(NODE)
        self.add_rich_content(new_content, NODE)

    @property
    def icons(self) -> List[Icon]:
        return icons_in(self.element)

    def add_icons(self, *icons: Icon):
        for icon in icons:
            SubElement(self.element, 'icon', BUILTIN=icon.name)

    def remove_icons(self, *icons):
        for icon in icons:
            i = self.element.find('icon[@BUILTIN="%s"]' % icon.name)
            if i is not None:
                self.element.remove(i)

    @property
    def link(self) -> str:
        """returns the hyperlink of a node."""
        return self.get(LINK)

    @link.setter
    def link(self, value: str):
        self.set(LINK, value)

    @property
    def note(self) -> RichText:
        """the note attached to a node

        :return: rich text from note
        """
        return self.find_rich_content_for(NOTE)

    @note.setter
    def note(self, new_content: str):
        self.remove_rich_content(NOTE)
        self.add_rich_content(new_content, NOTE)

    def set_text(self, text):
        self.set(TEXT, text)

    def set_link(self, link):
        self.set(LINK,link)

    def set_icons(self, icons):
        self.set(ICONS, icons if icons else [])

    def set(self, name, value):
        MapElement.set(self, name, value)
        if name not in [MODIFIED, ID]:
            self._update_modified()

    def _update_modified(self):
        self.element.set(MODIFIED, str(timestamp_in_millis(datetime.now())))

    @property
    def node_id(self) -> Optional[str]:
        """Unique id that identifies the node"""
        return self.get(ID)


    def all_branches(self):
        result = [self]
        for branch in self.branches():
            result += branch.all_branches()
        return result

    def remove_rich_content(self, node_type):
        rc = self.find_rich_content_element(node_type)
        if rc is not None:
            self.element.remove(rc)

    def add_rich_content(self, new_content: str, node_type):
        rt = RichText()
        rt.markdown = new_content
        self.element.append(rt.html_element(node_type))

class Connection(MapElement):

    def set_default_element(self):
        self.element = Element('node')

    @property
    def source_label(self):
        return self.get(SOURCE_LABEL)

    @source_label.setter
    def source_label(self, label: str):
        self.set(SOURCE_LABEL, label)

    @property
    def middle_label(self):
        return self.get(MIDDLE_LABEL)

    @middle_label.setter
    def middle_label(self, label: str):
        self.set(MIDDLE_LABEL, label)

    @property
    def target_label(self):
        return self.get(TARGET_LABEL)

    @target_label.setter
    def target_label(self, label: str):
        self.set(TARGET_LABEL, label)

    @property
    def start_inclination(self):
        return self.get(STARTINCLINATION)

    @start_inclination.setter
    def start_inclination(self, coordinates: str):
        self.set(STARTINCLINATION, coordinates)

    @property
    def end_inclination(self):
        return self.get(ENDINCLINATION)

    @end_inclination.setter
    def end_inclination(self, coordinates: str):
        self.set(ENDINCLINATION, coordinates)

