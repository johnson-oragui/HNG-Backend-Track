from user.models import User
from user_organisation.models import UserOrganisation


def retrieve_user(data: dict, requested_user_id):
    """
    Retrieves a user
    """
    try:
        token_user = get_user(data=data)
        if not token_user:
            return None

        user = sanitize_user(token_user)
        if user['id'] == requested_user_id:
            return user
        # retrieve the user that has id from params
        requested_user = get_user(user_id=requested_user_id)
        if not requested_user:
            return

        # check if the requested_user is a member in token_user's organisation
        is_authorized = is_token_user_authorized(token_user, requested_user)

        if not is_authorized:
            return
        # if token_user owns any organisation, return the requested_user
        user = sanitize_user(requested_user)
        return user
    except Exception as exc:
        print(f'could not retrieve user: {exc}')


def get_user(data=None, user_id=None):
    """
    Retrieves the user.
    """
    try:
        if data and not user_id:
            user = User.objects.get(email=data['email'], id=data['user_id'])
            return user
        elif not data and user_id:
            user = User.objects.get(id=user_id)
            return user
    except Exception as exc:
        print(f'error in get_user func: {exc}')


def sanitize_user(user_object: dict):
    """
    Removes sensitive information from the user data.
    """
    try:
        user = user_object.__dict__.copy()
        user.pop('password', None)
        user.pop('_state', None)
        user.pop('created_at', None)
        user.pop('updated_at', None)
        return user
    except Exception as exc:
        print(f'error in sanitize_user func: {exc}')

def is_token_user_authorized(token_user, requested_user):
    """
    Checks if the token user is authorized to access the requested user's data.
    """
    try:
        # retrieve all organisations token user created
        token_user_orgs = UserOrganisation.objects.filter(user=token_user, role="owner")
        # retrieve all organisations requested user is a member in
        requested_user_orgs = UserOrganisation.objects.filter(user=requested_user, role="member")

        # Convert the organisation to sets for faster comparison
        token_user_org_set = set(org.organisation for org in token_user_orgs)
        requested_user_org_set = set(org.organisation for org in requested_user_orgs)

        # check for common organisation
        common_org = token_user_org_set & requested_user_org_set

        return bool(common_org)
    except Exception as exc:
        print(f'error in is_token_user_authorized func: {exc}')
