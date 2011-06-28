# -*- coding: utf-8 -*-
# core.forms

from kay.utils import forms

class MyInputForm(forms.Form):
	tweet = forms.TextField(u'tweet', required=False)
	other_name = forms.TextField(u'other_name', required=False)


class MyUserForm(forms.Form):
	user_name = forms.TextField(u'ユーザー名', required=True)
	password = forms.TextField(u'パスワード',
		required=True, widget=forms.PasswordInput)
	password_confirm = forms.TextField(u'パスワードの再入力',
		required=True, widget=forms.PasswordInput)
	def context_validate(self, data):
		'''Confirm the password one another'''
		if data['password'] != data['password_confirm']:
			raise ValidationError(u'パスワードが一致しません。')

		return None

