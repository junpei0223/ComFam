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
from kay.generics.rest import RESTViewGroup
from kay.generics import (OP_LIST, OP_SHOW, OP_CREATE, OP_UPDATE, OP_DELETE)
from kay.generics import login_required

class MyRESTViewGroup(RESTViewGroup):
	models = ['core.models.Tweet']
	authorize = login_required
"""	以下はBasic認証を実装
	def authorize(self, request, operation, obj=None, model_name=None,
					prop_name=None):
		'''アクセス制限
		@param request: リクエスト
		@param operation: 処理(OP_LIST, OP_SHOW, OP_CREATE, OP_UPDATE, OP_DELETE)
		@param obj: 処理対象のオブジェクト(OP_SHOW, OP_UPDATE, OP_DELETEのときのみ)
		@param model_name: モデル名
		@param prop_name:
		@raise e: アクセスを許可しないときは kay.exceptions.NotAuthorized を投げる
		'''
		from kay.auth import login
		from kay.exceptions import NotAuthorized
		import base64
		auth_header = request.headers.get('Authorization')
		if not auth_header: raise NotAuthorized
		(scheme, base64str) = auth_header.split(' ')
		if scheme != 'Basic': raise NotAuthorized
		(username, password) = base64.b64decode(base64str).split(':')
		result = login(request, user_name = username, password = password)
		if not result: raise NotAuthorized
		#if not request.user.is_admin: raise NotAuthorized
		return True
"""

view_groups = [
	MyRESTViewGroup(),
	ViewGroup(
		Rule('/', endpoint='index', view='core.views.index'),
		Rule('/user_home', endpoint='user_home', view='core.views.user_home'),
		Rule('/new_user', endpoint='new_user', view='core.views.new_user'),
	)
]
