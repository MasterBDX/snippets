from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import UserProfile

User = get_user_model()


class UserModelTest(TestCase):
	def setUp(self):
		self.username = 'Masterbdx'
		self.phone_number = "218911123432"
		self.phone_number2 = "218911123433"
		self.user = User.objects.create(username=self.username,
										phone_number=self.phone_number,
										email="test@gmail.com")
		self.user2 = User.objects.create(username=self.username,phone_number=self.phone_number2)

	def test_user_slug(self):
		slug = self.username.lower()
		self.assertIsNotNone(self.user.slug)
		self.assertEqual(slug,self.user.slug)
		self.assertIsNotNone(self.user2.slug)
		self.assertNotEqual(slug,self.user2.slug)
		self.assertIn(slug,self.user2.slug)


class UserProfileModelTest(TestCase):
	def setUp(self):
		self.username = 'Masterbdx'
		self.user = User.objects.create(username=self.username)


	def test_user_profile_creater(self):
		profile = UserProfile.objects.filter(user=self.user)
		self.assertTrue(profile.exists())
		self.assertEqual(profile.first().user.username,self.username)




