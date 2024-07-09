from django.db import models
from django.utils.timezone import now
from api.models import MyUserModelManager
from uuid import uuid4


class User(models.Model):
    """
    Class to represent User in the table
    """
    objects = MyUserModelManager()
    id = models.CharField(primary_key=True, unique=True, null=False, auto_created=True, default=str(uuid4()), max_length=60)
    firstName = models.CharField(null=False, max_length=60)
    lastName = models.CharField(null=False, max_length=60)
    email = models.CharField(null=False, unique=True, max_length=60)
    password = models.CharField(null=False, max_length=60)
    phone = models.CharField(max_length=15)
    create_at = models.DateField(default=now)
    update_at = models.DateField(default=now)

    class Meta:
        """

        """
        db_table = "users"

    def __str__(self):
        """
        String representation of user
        """
        one = f"id: {self.id}, firstName: {self.firstName}, lastName: {self.lastName}, "
        two = f"email: {self.email}, password: {self.password}, phone: {self.phone}, "
        three = f"created_at: {self.create_at}, updated_at: {self.update_at}"
        return ("{" + one + '\n' + two + '\n' + three + "}")
