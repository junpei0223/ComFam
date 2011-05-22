# -*- coding: utf-8 -*-
# core.urls

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
	return [
		EndpointPrefix('core/', [
			Rule('/', endpoint='index'),
		]),
	]

all_views = {
	'core/index': 'core.views.index',
}
"""

from kay.routing import (
	ViewGroup, Rule
)

view_groups = [
	ViewGroup(
		Rule('/', endpoint='index', view='core.views.index'),
		Rule('/user_home', endpoint='user_home', view='core.views.user_home'),
	)
]
