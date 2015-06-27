import os.path as op

import yaml


MODULE_ROOT = op.dirname(__file__)


def load(path):
    with open(path, 'r') as fin:
        data = yaml.safe_load(fin)
        return data
