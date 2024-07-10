from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime
from user.models import User
from organisation.models import Organisation
from api.utils import gen_uuid_str


class UserOrganisation(models.Model):
    user_org_id = models.CharField(null=False, default=gen_uuid_str, max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(default=datetime.now)

    # Define choices for role with default as "owner"
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('member', 'Member'),
    )

    role = models.CharField(null=False, max_length=60, choices=ROLE_CHOICES, default='owner', blank=False)

    class Meta:
        """
        Enforce one-to-one user-organisation relationship within a membership
        """
        db_table = "user_organisations"
        # ordering = ['created_at']
        unique_together = (('user', 'organisation'),)

    @classmethod
    def owners(cls):
        """
        Retrieve all user-organisation relationships where the role is 'owner'.
        """
        return cls.objects.filter(role='owner')

    @classmethod
    def members(cls):
        """
        Retrieve all user-organisation relationships where the role is 'member'.
        """
        return cls.objects.filter(role='member')
