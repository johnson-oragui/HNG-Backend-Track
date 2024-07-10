from django.db import models
from django.utils.timezone import now
from api.models import MyUserModelManager
from api.utils import gen_uuid_str
from datetime import datetime


class User(models.Model):
    """
    Class to represent User in the table
    """
    objects = MyUserModelManager()
    id = models.CharField(primary_key=True, unique=True, null=False, auto_created=True, default=gen_uuid_str, max_length=80)
    firstName = models.CharField(null=False, max_length=60)
    lastName = models.CharField(null=False, max_length=60)
    email = models.EmailField(null=False, unique=True, max_length=60)
    password = models.CharField(null=False, max_length=80)
    phone = models.CharField(max_length=15)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(default=datetime.now)

    class Meta:
        """
        Defines meta dta for users table
        """
        db_table = "users"
