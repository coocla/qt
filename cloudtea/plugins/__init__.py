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
        for plugin_name in modules:
            try:
                plugin_name = '%(PLUGINS_DIR)s.%(plugin_name)s' % locals()
                plugin = importlib.import_module(plugin_name)
                # plugin_name = module.__alias__
                if plugin.check_policy(self.user):
                    # self._plugins[plugin_name] = module
                    plugin.enable(self._app, self.user)
                    logger.info('detect plugin %s' % plugin_name)
            except Exception as e:
                logger.error('detect a bad plugin %s, traceback:\n%s' % (plugin_name, e), exc_info=True)