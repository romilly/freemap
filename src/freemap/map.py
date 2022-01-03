from datetime import datetime as dt

from html2text import html2text
from lxml import etree
from lxml.etree import tostring, Element

from freemap.uuids import UUIDGenerator

MODIFIED = 'MODIFIED'

__author__ = 'romilly'


def datetime(timestamp_in_milliseconds):
    return dt.fromtimestamp(float(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


def build_node_from(element: Element):
    if element.tag == 'node':
        id_ = element.get('ID')
        branch = Branch()
        branch.set_id(id_)
        branch.set_created(element.get('CREATED'))
        branch.set_text(element.get('TEXT'))
        branch.set_localized_text(element.get('LOCALIZED_TEXT'))
        branch.set_markdown_text(find_rich_content_in(element, 'NODE'))
        branch.set_details_markdown(find_rich_content_in(element, 'DETAILS'))
        branch.set_link(element.get('LINK'))
        branch.set_icons(icons_in(element))
        branch.set_note(get_note_from(element)) # TODO: use find_rich_content
        branch.set_modified(element.get('MODIFIED'))
        return branch


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


def icons_in(child):
    return [Icons.icon(icon.get('BUILTIN')) for icon in child.findall('icon')]


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
    def __init__(self, root: Element):
        self._root = root
        root_node_xml = root.find('node')
        self.root_node = build_node_from(root_node_xml)
        add_children_from_xml(root_node_xml, self.root_node)

    def root(self) -> Element:
        return self.root_node

    def as_text(self) -> str:
        return tostring(self._root).decode('utf-8')

# TODO: note, description (currently missing) should contain None by default
# since a mind map file might contain a note or description with no text or a note.. with empty text.


class Branch:
    def __init__(self):
        self._node_id = UUIDGenerator.next_uuid()
        self._attributes = {}
        self.set_text(None)
        self.set_localized_text(None)
        self.set_icons([])
        self.set_link(None)
        self.set_note('')
        self._children = []
        timestamp_ms = self.timestamp(dt.now())
        self.set_created(timestamp_ms)

    def timestamp(self, now):
        return 1000 * now.timestamp()

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    def set_created(self, ts):
        self.set('CREATED', datetime(ts))

    def set_modified(self, ts):
        self._attributes[MODIFIED] = datetime(ts)

    def created(self):
        return self.get('CREATED')

    def detail_markdown(self):
        return self.get('DETAILS_MARKDOWN')

    def modified(self):
        return self.get('MODIFIED')

    def localized_text(self):
        return self.get('LOCALIZED_TEXT')

    def text(self):
        return self.get('TEXT')

    def icons(self):
        return self.get('ICONS')

    def link(self):
        return self.get('LINK')

    def markdown_text(self) -> str:
        return self.get('MARKDOWN_TEXT')

    def note(self):
        return self.get('NOTE')

    def set_text(self, text):
        self.set('TEXT', text)

    def set_localized_text(self, text):
        self.set('LOCALIZED_TEXT', text)

    def set_link(self, link):
        self.set('LINK',link)

    def set_icons(self, icons):
        self.set('ICONS', icons if icons else [])

    def set_note(self, note):
        self.set('NOTE', note if note else '')

    def set(self, name, value):
        self._attributes[name] = value
        if name != MODIFIED:
            self._attributes[MODIFIED] = dt.now()

    def get(self, name):
        if name in self._attributes:
            return self._attributes[name]
        return None

    def set_markdown_text(self, text):
        self._attributes['MARKDOWN_TEXT'] = text

    def set_details_markdown(self, text):
        self._attributes['DETAILS_MARKDOWN'] = text
        pass

    def set_id(self, id_):
        self._node_id = id_

    def id(self):
        return self._node_id




