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
    def __init__(self, id=None):
        self._children = []
        self.id = id if id else UUIDGenerator.nextUUID()
        self._created = dt.now()
        self._modified = dt.now()

    def datetime(self, timestamp_in_milliseconds):
        return dt.fromtimestamp(int(timestamp_in_milliseconds) / 1000.0)

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    def set_created(self, ts):
        self._created = ts

    def set_modified(self, ts):
        self._modified = ts

    def created(self):
        return self._created

    def modified(self):
        return self._modified


class Map(MapElement):
    def root(self):
        return self.branch(0)


class Branch(MapElement):
    def __init__(self, id):
        MapElement.__init__(self, id)
        self._text = ''
        self._icons = []
        self._link = None
        self._note = ''

    def text(self):
        return self._text

    def icons(self):
        return self._icons

    def link(self):
        return self._link

    def note(self):
        return self._note

    def set_text(self, text):
        self._text = text if text else ''

    def set_link(self, link):
        self._link = link

    def set_icons(self, icons):
        self._icons = icons if icons else []

    def set_note(self, note):
        self._note = note if note else ''


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
                new_branch = Branch(child_xml.get('ID'))
                new_branch.set_created(self.datetime(child_xml.get('CREATED')))
                new_branch.set_modified(self.datetime(child_xml.get('MODIFIED')))
                new_branch.set_text(child_xml.get('TEXT'))
                new_branch.set_link(child_xml.get('LINK'))
                new_branch.set_icons(self.icons_in(child_xml))
                new_branch.set_note(self.get_note_from(child_xml))
                child = parent.add_child(new_branch)
                self.add_children_from_xml(child_xml, child)
        return parent

    @classmethod
    def datetime(self, timestamp_in_milliseconds):
        return dt.fromtimestamp(int(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


    @classmethod
    def icons_in(self, child):
        return [Icons.icon(icon.get('BUILTIN')) for icon in child.findall('icon')]

    @classmethod
    def get_note_from(self, child_xml):
        rich_content = child_xml.find('richcontent')
        if rich_content is None:
            return None
        return etree.tostring(rich_content.find('html'))


