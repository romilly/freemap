from lxml import etree

from freemap.map import Branch, Icons, Map


def map_from_string(map_text: str):
    doc = etree.XML(map_text)
    return build_map_from_xml(doc)


def build_node_from_xml(child_xml):
    if child_xml.tag == 'node':
        branch = Branch(child_xml.get('ID'))
        branch.set_created(child_xml.get('CREATED'))
        branch.set_text(child_xml.get('TEXT'))
        branch.set_localized_text(child_xml.get('LOCALIZED_TEXT'))
        branch.set_link(child_xml.get('LINK'))
        branch.set_icons(icons_in(child_xml))
        branch.set_note(get_note_from(child_xml))
        branch.set_modified(child_xml.get('MODIFIED'))
        return branch


def build_map_from_xml(fm: etree.Element):
    root_node_xml = fm.find('node')
    root = build_node_from_xml(root_node_xml)
    add_children_from_xml(root_node_xml, root)
    return Map(root)


def add_children_from_xml(xml_node, parent):
    for child_xml in xml_node:
        if child_xml.tag == 'node':
            new_branch = build_node_from_xml(child_xml)
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

