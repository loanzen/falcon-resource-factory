# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import re

import six


def underscore_camelcase_converter(value):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), value)

