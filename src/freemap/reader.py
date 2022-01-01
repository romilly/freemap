from html2text import html2text
from lxml import etree

from freemap.map import Branch, Icons, Map

# TODO: handle html instead of text in nodes.
#

def map_from_string(map_text: str):
    doc = etree.XML(map_text)
    return build_map_from_xml(doc)


def build_node_from(xml):
    if xml.tag == 'node':
        branch = Branch(xml.get('ID'))
        branch.set_created(xml.get('CREATED'))
        branch.set_text(xml.get('TEXT'))
        branch.set_localized_text(xml.get('LOCALIZED_TEXT'))
        branch.set_markdown_text(find_rich_content_in(xml, 'NODE'))
        branch.set_details_markdown(find_rich_content_in(xml, 'DETAILS'))
        branch.set_link(xml.get('LINK'))
        branch.set_icons(icons_in(xml))
        branch.set_note(get_note_from(xml)) # TODO: use find_rich_content
        branch.set_modified(xml.get('MODIFIED'))
        return branch


def find_rich_content_in(xml, node_type):
    rc = xml.find('richcontent[@TYPE="%s"]' % node_type)
    if rc is not None:
        html = rc.find('html')
        text = etree.tostring(html)
        return html2text(text.decode('utf-8'))


def build_map_from_xml(fm: etree.Element):
    root_node_xml = fm.find('node')
    root = build_node_from(root_node_xml)
    add_children_from_xml(root_node_xml, root)
    return Map(root)


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

