from lxml import etree

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
    def __init__(self):
        self._branches = []

    def add_branch(self, branch):
        self._branches.append(branch)
        return branch

    def branches(self):
        return self._branches

    def branch(self, index):
        return self.branches()[index]


class Map(MapElement):
    def root(self):
        return self.branch(0)


class Branch(MapElement):
    def __init__(self, text, icons, link, note):
        MapElement.__init__(self)
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
        fm = etree.XML(map_text)
        root = Map()
        self.convert(fm, root)
        return root

    def convert(self, xml_node, parent):
        for child in xml_node:
            if child.tag == 'node':
                branch = parent.add_branch(
                    Branch(child.get('TEXT'), self.icons_in(child), child.get('LINK'), self.get_note_from(child)))
                self.convert(child, branch)

    def icons_in(self, child):
        return [Icons.icon(icon.get('BUILTIN')) for icon in child.findall('icon')]

    def get_note_from(self, child):
        rich_content = child.find('richcontent')
        if rich_content is None:
            return None
        return etree.tostring(rich_content.find('html'))


