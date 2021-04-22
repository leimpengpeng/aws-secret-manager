
import yaml
import os
from os import path as osp
_config = None

def get_config():
    global _config
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    config_yaml = osp.join(BASE_DIR, 'config/config.yaml')
    with open(config_yaml, "r") as ymlfile:
        _config = yaml.safe_load(ymlfile)
    return _config
    
def get_common_config():
    common_config = get_config()
    return common_config.get('common', None)
