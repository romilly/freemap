from lxml import etree
from freemind.map import Branch, Icons, Map
from datetime import datetime as dt


class MapReader():
    def __init__(self):
        pass

    def read(self, map_text):
        return self.build_map_from_xml(etree.XML(map_text))

    def build_node_from_xml(self, child_xml):
        if child_xml.tag == 'node':
            branch = Branch(child_xml.get('ID'), dt.now())
            branch.set_created(child_xml.get('CREATED'))
            branch.set_text(child_xml.get('TEXT'))
            branch.set_link(child_xml.get('LINK'))
            branch.set_icons(self.icons_in(child_xml))
            branch.set_note(self.get_note_from(child_xml))
            branch.set_modified(child_xml.get('MODIFIED'))
            return branch

    def build_map_from_xml(self, fm):
        root = self.build_node_from_xml(fm[0])
        self.add_children_from_xml(fm[0], root)
        return Map(root)

    def add_children_from_xml(self, xml_node, parent):
        for child_xml in xml_node:
            if child_xml.tag == 'node':
                new_branch = self.build_node_from_xml(child_xml)
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
        return etree.tostring(rich_content.find('html'), encoding=str)

