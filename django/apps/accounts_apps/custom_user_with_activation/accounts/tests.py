from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserTest(TestCase):
	def setUp(self):
		self.username = 'Masterbdx'
		self.email = 'masterbdxteam@gmail.com'
		self.user = User.objects.create(username=self.username,
										email=self.email,
										)

	def test_user_slug(self):
		username = self.username.lower()
		self.assertIsNotNone(self.user.slug)
		self.assertIn(username,self.user.slug)







