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
from forms import (MyInputForm, MyUserForm)

# Max number of items / page
ITEMS_PER_PAGE = 20


def index(request):
	form = MyUserForm()
	msg = None
	if request.method == 'POST':
		'''
		if form.validate(request.form):
			try:
				create_new_user(form['user_name'],
								password=form['password'])
				msg = u'ユーザーを登録しました。'
			except DuplicateKeyError:
				msg = u'既に同じユーザー名が登録されています。'
		'''
		pass
	elif request.method == 'GET':
		if request.user.is_anonymous() == False:
			return redirect(url_for('core/user_home'))
	return render_to_response('core/index.html',
					{'form': form.as_widget(),
					'msg': msg,
					'users': MyUser.all()})


@login_required
def user_home(request):
	form = MyInputForm()
	msg = None
	my_board = Board.gql("WHERE name = '%s'"
					% str(request.user)).get()
	if request.method == 'POST':
		if form.validate(request.form):
			# tweet.author is auto-created.
			if form['tweet'] == '':
					pass
			else:
				tweet = Tweet(tweet=form['tweet'])
				if my_board == None:
					# My tweet must belog to this board object.
					my_board = Board(name=str(request.user))
					my_board.put()
				tweet.boards.append(my_board.key())
				for o in my_board.others:
					tweet.boards.append(o)
				tweet.put()
				if form['other_name'] != None:
					rtn = join_board(str(request.user), form['other_name'])
			form.reset()
	elif request.method == 'GET':
		pass
	return render_to_response('core/user_home.html',
					{'form': form.as_widget(),
					'msg': msg,
					'my_board': my_board})


def new_user(request):
	form = MyUserForm()
	if request.method == 'POST':
		if form.validate(request.form):
			try:
				create_new_user(form['user_name'],
								password=form['password'])
				msg = u'ユーザーを登録しました。'
				return redirect(url_for('core/user_home'))
			except DuplicateKeyError:
				msg = u'既に同じユーザー名が登録されています。'
	
	return render_to_response('core/new_user.html',
					{'form': form.as_widget()})


def join_board(my_name,other_name):
	'''
	Return of True means that other_tweets are added to my board.
	Oppsitely, return of False means Failure of addision to my board happened.
	'''
	if my_name == other_name:
		return False
	my_board = Board.gql("WHERE name = '%s'" % my_name).get()
	other_board = Board.gql("WHERE name = '%s'" % other_name).get()
	if my_board == None or other_board == None:
		return False
	if other_board.key() in my_board.others:
		return False
	other_tweets = other_board.tweets
	for t in other_tweets:
		if not my_board.key() in t.boards:
			t.boards.append(my_board.key())
			t.put()
	my_board.others.append(other_board.key())
	my_board.put()
	return True

