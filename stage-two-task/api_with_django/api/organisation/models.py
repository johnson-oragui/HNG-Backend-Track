from django.db import models
from django.utils.timezone import now
from api.utils import gen_uuid_str


class Organisation(models.Model):
    id = models.CharField(primary_key=True, unique=True, null=False, default=gen_uuid_str, auto_created=True, max_length=60)
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(max_length=1000)
    owner_email = models.EmailField(null=False, blank=False, max_length=60)
    create_at = models.DateField(default=now)
    update_at = models.DateField(default=now)

    class Meta:
        db_table = "organisations"
