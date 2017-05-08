# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division

import re

import six


def camelcase_underscore_converter(value):

    if not isinstance(value, six.string_types):
        raise ValueError('Invalid type.')

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def underscore_camelcase_converter(value):
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), value)

