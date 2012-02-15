from google.appengine.ext import db
from kay.ext.testutils.gae_test_base import GAETestBase
from core.models import Tweet

class TweetTest(GAETestBase):
	#All entities are deleted when you finished tests.
	CLEANUP_USED_KIND = True

	def test_model(self):
		t = Tweet(tweet='a')
		t.put()
		tweets = Tweet.all().fetch(100)
		self.assertEquals(len(tweets),1)
		tt = Tweet.get(t.key())
		self.assertEquals(tt.tweet, 'a')

