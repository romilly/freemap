from datetime import datetime as dt
from freemap.uuids import UUIDGenerator

MODIFIED = 'MODIFIED'

__author__ = 'romilly'


def datetime(timestamp_in_milliseconds):
    return dt.fromtimestamp(float(timestamp_in_milliseconds) / 1000.0) if timestamp_in_milliseconds else None


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
        self.id = id if id else UUIDGenerator.next_uuid()


class Map():
    def __init__(self, root):
        self._root = root

    def root(self):
        return self._root


class Branch(MapElement):
    def __init__(self, id):
        MapElement.__init__(self, id)
        self._attributes = {}
        self.set_text('')
        self.set_icons([])
        self.set_link(None)
        self.set_note('')
        self._children = []
        timestamp_ms = self.timestamp(dt.now())
        self.set_created(timestamp_ms)

    def timestamp(self, now):
        return 1000 * now.timestamp()

    def add_child(self, branch):
        self._children.append(branch)
        return branch

    def branches(self):
        return self._children

    def branch(self, index):
        return self.branches()[index]

    def set_created(self, ts):
        self.set('CREATED', datetime(ts))

    def set_modified(self, ts):
        self._attributes[MODIFIED] = datetime(ts)

    def created(self):
        return self.get('CREATED')

    def modified(self):
        return self.get('MODIFIED')

    def text(self):
        return self.get('TEXT')

    def icons(self):
        return self.get('ICONS')

    def link(self):
        return self.get('LINK')

    def note(self):
        return self.get('NOTE')

    def set_text(self, text):
        self.set('TEXT', text if text else '')

    def set_link(self, link):
        self.set('LINK',link)

    def set_icons(self, icons):
        self.set('ICONS', icons if icons else [])

    def set_note(self, note):
        self.set('NOTE', note if note else '')

    def set(self, name, value):
        self._attributes[name] = value
        if name != MODIFIED:
            self._attributes[MODIFIED] = dt.now()

    def get(self, name):
        return self._attributes[name]



