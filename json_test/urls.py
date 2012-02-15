# -*- coding: utf-8 -*-
# json_test.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('json_test/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'json_test/index': 'json_test.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='json_test.views.index'),
  )
]

