from hamcrest.core.base_matcher import BaseMatcher


class Between(BaseMatcher):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def _matches(self, item):
        return self.low <= item <= self.high

    def describe_to(self, description):
        description.append_text('a value between %s and %s' % (self.low, self.high))


def between(low, high):
    return Between(low, high)