from datetime import datetime
from lxml import etree

from freemind.uuids import UUIDGenerator

__author__ = 'romilly'


class Icon():
    def __init__(self, name):
        self._name = name


class Icons(object):
    icons = {}

    @classmethod
    def icon(cls, name):
        if name not in cls.icons:
            cls.icons[name] = Icon(name)
        return cls.icons[name]


class MapElement():
    def __init__(self, id=None, created=None):
        self._children = []
        self.id = id if id else UUIDGenerator.nextUUID()
        self.created = datetime.fromtimestamp(int(created)/1000.0) if created else datetime.now()

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]


class Map(MapElement):
    def root(self):
        return self.branch(0)


class Branch(MapElement):
    def __init__(self, id, created, text, link, icons, note):
        MapElement.__init__(self, id, created)
        self._text = text
        self._icons = icons
        self._link = link
        self._note = note

    def text(self):
        return self._text

    def icons(self):
        return self._icons

    def link(self):
        return self._link

    def note(self):
        return self._note


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
                child = parent.add_child(
                    Branch(child_xml.get('ID'),
                           child_xml.get('CREATED'),
                           child_xml.get('TEXT'),
                           child_xml.get('LINK'),
                           self.icons_in(child_xml),
                           self.get_note_from(child_xml)))
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


