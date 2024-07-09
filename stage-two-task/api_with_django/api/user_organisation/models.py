from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from user.models import User
from organisation.models import Organisation


class UserOrganisation(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    create_at = models.DateField(default=now)
    update_at = models.DateField(default=now)

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

    def owners(self):
        """

        """
        return self.filter(role='owner')

    def __str__(self):
        return f"{self.user.email} - {self.organisation.name} ({self.role})"
