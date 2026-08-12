from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


def _now():
    return timezone.now()


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str max length=20
        param last_name: Describes last name of the user
        type last_name: str max length=20
        param middle_name: Describes middle name of the user
        type middle_name: str max length=20
        param email: Describes the email of the user
        type email: str, unique, max length=100
        param password: Describes the password of the user
        type password: str
        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int (timestamp)
        param updated_at: Describes the date when the user was modified
        type updated_at: int (timestamp)
        param role: user role, default role (0, 'visitor')
        type role: int (choices)
        param is_active: default value False
        type is_active: bool

    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(editable=False, default=_now)
    updated_at = models.DateTimeField(default=_now)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'first_name'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def clean(self):
        valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", self.email)
        if not valid_email:
            raise ValidationError("Invalid email")
        

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        fields = {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }
        return str(fields)[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.pk})"

    @classmethod
    def get_by_id(cls, user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_by_email(cls, email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_by_id(cls, user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            cls.objects.get(pk=user_id).delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def create(cls, email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        obj = cls(
            email=email, password=password, first_name=first_name,
            middle_name=middle_name, last_name=last_name)
        try:
            obj.save()
            return obj
        except ValidationError:
            return

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'role': 0,
        |   'is_active': True
        | }
        """
        fields = {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }
        return fields

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        for name, value in locals().items():
            if name != "self" and value is not None:
                setattr(self, name, value)
        self.updated_at = _now()
        try:
            self.save()
        except ValidationError:
            return

    @classmethod
    def get_all(cls):
        """
        returns data for json request with QuerySet of all users
        """
        return cls.objects.all()

    def get_role_name(self):
        """
        returns str role name
        """
        return self.get_role_display()