# -*- coding: utf-8 -*-
# core.views

from kay.utils import (render_to_response, forms, url_for)
from kay.utils.validators import ValidationError
from kay.auth import (create_new_user, DuplicateKeyError)
from kay.auth.decorators import login_required
from kay import dbutils
from werkzeug import (redirect, Response)
from google.appengine.ext import db
from google.appengine.api import (users, memcache, channel)
from core.models import (MyUser, Tweet, Board)
from core.forms import (MyInputForm, MyUserForm, FriendsForm)
import logging
import json

def index(request):
	form = MyUserForm()
	
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		if request.user.is_anonymous() == False:
			return redirect(url_for('core/user_home'))
	
	return render_to_response('core/index.html',
					{'form': form.as_widget(),
					'users': MyUser.all()})


def get_tweet(t):
	tweet_info = {
		'tweet': t.tweet,
		'author_user_name': t.author.user_name,
		'created_t': t.created_t
	}
	return json.encode(tweet_info)


@login_required
def user_home(request):
	# create token
	token = channel.create_channel(str(request.user.key()))

	# make author_list
	author_list = []
	author_list.append(request.user.key())
	user_info = MyUser.gql("WHERE user_name = :1",
							str(request.user)).get()
	#user_info = MyUser.get_by_key_name(request.user.key())
	if user_info:
		# logging.debug('author_list>>%s' % str(user_info.friends) )
		for f in user_info.friends:
			author_list.append(f)

	form = MyInputForm()	
	if request.method == 'POST':
		logging.debug('data>>%s' % request.values.get('data') )
		if form.validate(request.form):
			# tweet.author is auto-created.
			if form['tweet'] == '':
					pass
			else:
				tweet = Tweet(tweet=form['tweet'])
				#logging.debug('tweet>>%s' % tweet.tweet )
				tweet.put()
				# send message to others
				message = get_tweet(tweet)
				#logging.debug('message>>%s' % str(message))
				for l in author_list:
					if l != request.user.key():
						#logging.debug('send_messaget>>%s' % str(l) )
						channel.send_message(str(l),message)
		else:
			data = request.values.get('data')
			if data == None or data == '':
				pass
			else:
				tweet = Tweet(tweet=data)
				tweet.put()
				message = get_tweet(tweet)
				for l in author_list:
					if l != request.user.key():
						#logging.debug('send_messaget>>%s' % str(l) )
						channel.send_message(str(l),message)

		form.reset()
	elif request.method == 'GET':
		pass

	# get tweets
	tweets = Tweet.gql("WHERE author IN :1 ORDER BY created DESC LIMIT 15", author_list)
	
	# rendar html
	return render_to_response('core/user_home.html',
					{'form': form.as_widget(),
					'tweets': tweets,
					'token': token})


@login_required
def set_friends(request):
	form = FriendsForm()

	if request.method == 'POST':
		if form.validate(request.form):
			# set friends key
			user_info = MyUser.gql("WHERE user_name = :1",
									str(request.user)).get()
			f = MyUser.gql("WHERE user_name = :1",
									form['friend']).get()
			# logging.debug('set_friends>>%s' % f.key() )
			if f.key() not in user_info.friends:
				user_info.friends.append(f.key())
				user_info.put()

	return render_to_response('core/set_friends.html',
					{'form': form.as_widget()})


def new_user(request):
	form = MyUserForm()

	if request.method == 'POST':
		if form.validate(request.form):
			try:
				create_new_user(form['user_name'],
								password=form['password'])
				# msg = u'ユーザーを登録しました。'
				return redirect(url_for('core/index'))
			except DuplicateKeyError:
				# msg = u'既に同じユーザー名が登録されています。'
				pass
		
	return render_to_response('core/new_user.html',
					{'form': form.as_widget()})


def join_board(my_name,other_name):
	'''
	True Return means that other_tweets are added to my board.
	Oppsitely, False Return means that Failure of addision to my board happened.
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


def json_test(request):
	ts = Tweet.all()
	json = simplejson.dumps([dbutils.to_dict(t) for t in ts])
	return Response(json,content_type="application/json")


