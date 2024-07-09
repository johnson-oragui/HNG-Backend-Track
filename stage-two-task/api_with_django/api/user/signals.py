from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now
from django.dispatch import receiver
from user.models import User
from organisation.models import Organisation


@receiver(post_save, sender=User)
def auto_create_organisation_and_user_organisation(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    Auto creates an organisation and add user and organisation
    to the user_organisation table.

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
            org_name = f"{instance.firstName}'s Organisation"
            description = f"{instance.firstName}'s Organisation is the Greatest"

            # Create Organisation
            Organisation.objects.create(
                name=org_name,
                owner_email=instance.email,
                description=description
            )
    except Exception as exc:
        print(f'error occured: {exc}')
        raise Exception(
            "Could not auto create organisation and user_organisation from newly created user"
            ) from exc
    finally:
        print('end of post_save signal for user creation!')

@receiver(pre_save, sender=User)
def update_updated_at_field(sender, instance, **kwargs):
    """
    Updates user's updated_at field before update
    """
    try:
        if instance.pk:
            instance.updated_at = now()
    except Exception as exc:
        print(f'error updating user: {exc}')
        raise Exception(
            "Could not updating user"
            ) from exc
    finally:
        print('end of pre_save signal for user update!')
