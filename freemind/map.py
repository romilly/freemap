from datetime import datetime as dt
from lxml import etree

from freemind.uuids import UUIDGenerator

__author__ = 'romilly'


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


class MapElement():
    def __init__(self, id=None, created=None, modified=None):
        self._children = []
        self.id = id if id else UUIDGenerator.nextUUID()
        self._created = self.datetime_from_timestamp_default_now(created)
        self._modified = self.datetime_from_timestamp_default_now(modified)

    def datetime_from_timestamp_default_now(self, timestamp_in_milliseconds):
        return dt.fromtimestamp(int(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else dt.now()

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    def created(self):
        return self._created

    def modified(self):
        return self._modified


class Map(MapElement):
    def root(self):
        return self.branch(0)


class Branch(MapElement):
    def __init__(self, id, created, modified):
        MapElement.__init__(self, id, created, modified)
        self._text = None
        self._icons = []
        self._link = None
        self._note = None

    def text(self):
        return self._text

    def icons(self):
        return self._icons

    def link(self):
        return self._link

    def note(self):
        return self._note

    def set_text(self, text):
        self._text = text

    def set_link(self, link):
        self._link = link

    def set_icons(self, icons):
        self._icons = icons

    def set_note(self, note):
        self._note = note


class MapReader():
    def __init__(self):
        pass

    def read(self, map_text):
        return self.build_map_from_xml(etree.XML(map_text))

    def build_map_from_xml(self, fm):
        return self.add_children_from_xml(fm, Map())

    def add_children_from_xml(self, xml_node, parent):
        for child_xml in xml_node:
            if child_xml.tag == 'node':
                new_branch = Branch(child_xml.get('ID'),
                           child_xml.get('CREATED'),
                           child_xml.get('MODIFIED'))
                new_branch.set_text(child_xml.get('TEXT'))
                new_branch.set_link(child_xml.get('LINK'))
                new_branch.set_icons(self.icons_in(child_xml))
                new_branch.set_note(self.get_note_from(child_xml))
                child = parent.add_child(new_branch)
                self.add_children_from_xml(child_xml, child)
        return parent

    @classmethod
    def icons_in(self, child):
        return [Icons.icon(icon.get('BUILTIN')) for icon in child.findall('icon')]

    @classmethod
    def get_note_from(self, child_xml):
        rich_content = child_xml.find('richcontent')
        if rich_content is None:
            return None
        return etree.tostring(rich_content.find('html'))


