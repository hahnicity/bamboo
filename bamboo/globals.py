"""
bamboo.globals
~~~~~~~~~~~~~
"""
from peak.util.proxies import CallbackProxy
from bamboo.context import context

# Serves as a global paypal configuration object for the app
engine = CallbackProxy(lambda: context["engine"])
