from lxml.etree import tostring

from freemap.map import Map


class Writer:
    def as_text(map: Map) -> str:
        return tostring(map.root())
