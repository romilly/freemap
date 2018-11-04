import uuid

class UUIDGenerator():
    sequence = 0

    @classmethod
    def nextUUID(cls):
        cls.sequence += 1
        return uuid.uuid1(node=None, clock_seq=cls.sequence)