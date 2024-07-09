from django.db.models.signals import pre_delete, pre_save
from django.utils.timezone import now
from django.dispatch import receiver
# from django.core.exceptions import PermissionDenied
from user_organisation.models import UserOrganisation


@receiver(pre_delete, sender=UserOrganisation)
def confirm_owner_before_delete(sender, instance, using, **kwargs):
    """
    Confirms that the row been deleted is by the owner

    Params:
        sender: The model instance that has been created and saved
        instance: The model object that was created
        using: The database alias being used.
        origin: The origin of the deletion being the instance of a Model or QuerySet class.
    """
    if not instance.role == 'owner':
        raise PermissionError(
        f"Could not delete user_organisation, must be the owner to delete!: {instance.role}"
        )

@receiver(pre_save, sender=UserOrganisation)
def update_updated_at_field(sender, instance, **kwargs):
    """

    """
    try:
        if instance.pk:
            instance.updated_at = now()
    except Exception as exc:
        print(f'error updating user_organisation: {exc}')
        raise Exception(
            "Could not updating user_organisation"
            ) from exc
