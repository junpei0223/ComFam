# -*- coding: utf-8 -*-
# core.views

from kay.utils import (render_to_response, forms, url_for)
from kay.utils.validators import ValidationError
from kay.auth import (create_new_user, DuplicateKeyError)
from models import (MyUser, Tweet, Board)
from kay.auth.decorators import login_required
from werkzeug import redirect
from google.appengine.ext import db
import logging
from google.appengine.api import users

# Max number of items / page
ITEMS_PER_PAGE = 20


def index(request):
	form = MyUserForm()
	msg = None
	
	if request.method == 'POST':
		if form.validate(request.form):
			try:
				create_new_user(form['user_name'],
								password=form['password'])
				msg = u'ユーザーを登録しました。'
			except DuplicateKeyError:
				msg = u'既に同じユーザー名が登録されています。'
	elif request.method == 'GET':
		if request.user.is_anonymous() == False:
			return redirect(url_for('core/user_home'))

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

	def context_validate(self, data):
		'''Confirm the password one another'''
		if data['password'] != data['password_confirm']:
			raise ValidationError(u'パスワードが一致しません。')

		return None

@login_required
def user_home(request):
	form = MyInputForm()
	msg = None

	if request.method == 'POST':
		if form.validate(request.form):
			# tweet.author is auto-created.
			tweet = Tweet(tweet=form['tweet'])
			my_board = Board.gql("WHERE name = '%s'"
							% str(request.user)).get()
			if my_board == None:
				# My tweet must belog to this board object.
				my_board = Board(name=str(request.user))
				my_board.put()
			tweet.boards.append(my_board.key())
			tweet.put()
	elif request.method == 'GET':
		pass

	query = Tweet.gql("WHERE author = :1"
						" ORDER BY created DESC", request.user)
	tweet_all = query.fetch(ITEMS_PER_PAGE)

	return render_to_response('core/user_home.html',
					{'form': form.as_widget(),
					'msg': msg,
					'tweet_all': tweet_all})


class MyInputForm(forms.Form):
	tweet = forms.TextField(u'tweet', required=True)


def join_board(request):
	'''
	Return of True means that other_tweets are added to my board.
	Oppsitely, return of False means Failure of addision to my board happened.
	'''
	my_board = Board.gql("WHERE name = '%s'" % str(request.user)).get()
	other_board = Board.gql("WHERE name = '%s'" % other_name).get()
	if my_board == None or other_board == None:
		return False
	
	other_tweets = other_board.tweets()
	for t in other_tweets:
		if not my_board.key() in t.boards:
			t.boards.append(my_board.key())

	return True
