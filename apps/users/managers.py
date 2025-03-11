from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        validate_email(email)
        email = email.lower()
        user = self.model(
            email=email,
            **kwargs
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user