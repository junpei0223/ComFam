# -*- coding: utf-8 -*-
"""
core.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

from kay.utils import render_to_response
from kay.utils import forms
from kay.utils.validators import ValidationError
from kay.auth import (create_new_user, DuplicateKeyError)
from models import MyUser
from kay.auth.decorators import login_required

# Create your views here.

def index(request):
	form = MyUserForm()
	msg = None
	if request.method == 'POST':
		if form.validate(request.form):
			try:
				create_new_user(form['user_name'], 
								password=form['password'])
								#address=form['address'])
				msg = u'ユーザーを登録しました。'
			except DuplicateKeyError:
				msg = u'既に同じユーザー名が登録されています。'

	if request.method == 'GET':
		if request.user.is_anonymous() == False:
			return render_to_response('core/user_home.html',
							{'msg': msg})

	return render_to_response('core/index.html',
					{'form': form.as_widget(),
					'msg': msg,
					'users': MyUser.all()})

class MyUserForm(forms.Form):
	user_name = forms.TextField(u'ユーザー名', required=True)
	password = forms.TextField(u'パスワード',
	required=True, widget=forms.PasswordInput)
	password_confirm = forms.TextField(u'パスワードの再入力',
	required=True, widget=forms.PasswordInput)
#	address = forms.TextField(u'住所', required=True)

	def context_validate(self, data):
		'''パスワードの再入力チェック'''
		if data['password'] != data['password_confirm']:
			raise ValidationError(u'パスワードが一致しません。')

@login_required
def user_home(request):
	msg = None
	return render_to_response('core/user_home.html',
					{'msg': msg})
