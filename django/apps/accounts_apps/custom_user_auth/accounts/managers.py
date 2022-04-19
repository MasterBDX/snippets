from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        '''
            Create normal user object  
        '''
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None):
        '''
            Create staff user
            normal user object with is_staff attr == True
        '''
        user = self.create_user(
            email, username, password=password, is_staff=True)
        return user

    def create_superuser(self, email, username, password=None):
        '''
            Create Admin user
            Super user account
        '''
        user = self.create_user(email, username,
                                password=password,
                                is_staff=True,
                                is_admin=True)
        return user
