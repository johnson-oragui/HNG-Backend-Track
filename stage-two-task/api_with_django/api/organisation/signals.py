from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now
from django.dispatch import receiver
from user.models import User
from organisation.models import Organisation
from user_organisation.models import UserOrganisation


@receiver(post_save, sender=Organisation)
def auto_create_user_organisation(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    Auto creates user_organisation after organisation creation.

    Params:
        sender: The model instance that has been created and saved
        instance: The model object that was created
        created: A Truthy value signifying model successful creation
        raw: A boolean; True if the model is saved exactly as presented
        using: The database alias being used.
        update_fields: set of fields to update if model is been updated
        kwargs: Any kwargs that follows
    """
    try:
        if created:
            user = User.objects.get(email=instance.owner_email)
            # Create UserOrganisation
            UserOrganisation.objects.create(
                user=user,
                organisation=instance,
                role='owner'
            )
    except Exception as exc:
        print(f'error creating user_organisation: {exc}')
        raise Exception(
            "Could not auto create user_organisation from newly created organisation"
            ) from exc
    finally:
        print('end of post_save signal for organisation creation!')

@receiver(pre_save, sender=Organisation)
def update_updated_at_field(sender, instance, **kwargs):
    """

    """
    try:
        if instance.pk:
            instance.updated_at = now()
    except Exception as exc:
        print(f'error updating organisation: {exc}')
        raise Exception(
            "Could not updating organisation"
            ) from exc
    finally:
        print('end of pre_save signal for organisation update!')
