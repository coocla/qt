#coding:utf-8
import os
import importlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PluginsManager(object):
    def __init__(self, app, user=None):
        super(PluginsManager, self).__init__()
        self._app = app
        self.user = user
        self._plugins = {}

    def enable(self, plugin):
        plugin.enable(self._app)

    def disable(self, plugin):
        plugin.disable(self._app)

    def load_plugins(self):
        PLUGINS_DIR = 'plugins'
        modules = [p for p in os.listdir(PLUGINS_DIR) if os.path.isdir(os.path.join(PLUGINS_DIR, p))]
        print modules
        for module_name in modules:
            try:
                module_name = '%(PLUGINS_DIR)s.%(module_name)s' % locals()
                module = importlib.import_module(module_name)
                plugin_name = module.__alias__
                if module.check_policy(self.user):
                    self._plugins[plugin_name] = module
                    module.enable(self._app)
                    logger.info('detect plugin %s' % module_name)
            except Exception,e:
                logger.error('detect a bad plugin %s, traceback:\n%s' % (module_name, e), exc_info=True)