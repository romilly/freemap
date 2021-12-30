from xml.etree import ElementTree

from freemap.map import Map


class Writer:
    def as_text(map: Map) -> str:
        return ElementTree.tostring(map.root())
