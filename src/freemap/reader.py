from lxml import etree

from freemap.map import Map


def map_from_string(map_text: str):
    root = etree.XML(map_text)  # root is a map element
    return build_map_from_xml(root)


def build_map_from_xml(root: etree.Element):
    return Map(root)

