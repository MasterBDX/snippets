from django.test import TestCase
from ..forms import UserAdminCreationForm
from ..models import User

class AccountsFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="MasterBDX",
                                        phone_number="+218946325551",
                                        email="masterbdx@gmail.com")

    def test_admin_creation_form(self):
        invalid_form = UserAdminCreationForm(data={
                    "phone_number":"218925363661",
                    "username":"MasterBDX",
                    "password1":"12345%$#@!",
                    "password2":"12345%$#"})

        valid_form = UserAdminCreationForm(data={
                            "phone_number":"+218925363661",
                            "username":"MasterBDX",
                            "password1":"12345%$#@!",
                            "password2":"12345%$#@!"
                            })
        self.assertTrue(valid_form.is_valid())
        self.assertEqual(len(invalid_form.errors),2)
