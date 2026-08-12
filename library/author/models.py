from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20

    """
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    USERNAME_FIELD = 'name'

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        fields = ("id", "name", "surname", "patronymic")
        return str({field: getattr(self, field) for field in fields})[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.pk})"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @classmethod
    def get_by_id(cls, author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            return cls.objects.get(pk=author_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_by_id(cls, author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            cls.objects.get(pk=author_id).delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def create(cls, name, surname, patronymic):
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        obj = cls(name=name, surname=surname, patronymic=patronymic)
        try:
            obj.save()
            return obj
        except ValidationError:
            return

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
        fields = ("id", "name", "surname", "patronymic")
        return {field: getattr(self, field) for field in fields}

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Updates author in the database with the specified parameters.
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """
        for field, value in locals().items():
            if field != "self" and value is not None:
                setattr(self, field, value)
        try:
            self.save()
        except ValidationError:
            return

    @classmethod
    def get_all(cls):
        """
        returns data for json request with QuerySet of all authors
        """
        return cls.objects.all()