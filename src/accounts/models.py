from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=300,
                                validators=[RegexValidator(regex=USERNAME_REGEX,
                                                           message='Username must be alphanumeric or contain numbers',
                                                           code='invalid_username'
                                                           )
                                            ],
                                unique=True
                                )
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
