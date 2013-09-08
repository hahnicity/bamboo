"""
bamboo.globals
~~~~~~~~~~~~~
"""
from peak.util.proxies import CallbackProxy
from bamboo.context import context

db = CallbackProxy(lambda: context["db"])
