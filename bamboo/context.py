"""
bamboo.context
~~~~~~~~~~~~~~~~
"""
from peak.util.proxies import ObjectProxy

from bamboo import constants
from bamboo.attributes import AttributeDict

context = ObjectProxy(None)


class Context(AttributeDict):
    def __init__(self, **kwargs):
        self.update(kwargs)

    def push(self):
        """
        Push the configuration to the global proxy
        """
        if context.__subject__ is not self:
            context.__subject__ = self
        return self

    def pop(self):
        """
        Reset the configuration object to its initial state
        """
        if context.__subject__ is self:
            context.__subject__ = None

    def __enter__(self):
        return self.push()

    def __exit__(self, type, val, tb):
        self.pop()


def bamboo_context(**kwargs):
    """
    Initialize the context manager
    """
    return Context(**kwargs)
