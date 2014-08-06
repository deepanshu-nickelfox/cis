from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager, Group
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django_extensions.db.models import TimeStampedModel
from cis import signals
from hr.models import Position


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(*args, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    MALE = True
    FEMALE = False

    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    sex = models.NullBooleanField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    position = models.ForeignKey(
        Position, null=True, blank=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def fio(self):
        return u'{last_name} {first_name} {middle_name}'.format(
            last_name=self.last_name,
            first_name=self.first_name,
            middle_name=self.middle_name
        )

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.fio

    class Meta:
        permissions = (
            ("read_user", "Can read user"),
        )


pre_save.connect(
    signals.sync_user_groups_when_position_changes,
    sender=User)

post_save.connect(
    signals.sync_user_groups_when_user_created_with_position,
    sender=User)

pre_save.connect(
    signals.sync_user_groups_when_department_changes,
    sender=Position)

m2m_changed.connect(
    signals.admin_department_sync_workaround, sender=User.groups.through)
