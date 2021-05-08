import os
import shutil

from Utils.PluginLoad import load_plugins_in


def get_rule_plugins():
    plugin_dir = os.path.join('plugins', 'rules')
    rules = load_plugins_in(plugin_dir)
    return {rule.__name__: rule for rule in rules}


