from user_organisation.models import UserOrganisation
from organisation.models import Organisation
from user.models import User
from authentication.utils import escape_data


def get_organzations(data: dict):
    """
    Retrieves all organzations
    """
    try:
        all_org = Organisation.objects.filter(owner_email=data.get('email'))
        all_orgs = sanitize_organzations(all_org)
        return all_orgs
    except Exception as exc:
        print(f'error retrieving all organiztions: {exc}')

def sanitize_organzations(all_orgs: list = None, org: dict = None):
    """
    Retrieves all organzations
    """
    try:
        if not all_orgs and org:
            org_ins: dict = org.__dict__.copy()

            org_ins.pop('password', None)
            org_ins.pop('_state', None)
            org_ins.pop('created_at', None)
            org_ins.pop('updated_at', None)
            org_ins.pop('owner_email', None)

            org_ins['orgId'] = org_ins['id']
            org_ins.pop('id', None)
            return org_ins
        all_org = []
        for org in all_orgs:
            org_ins: dict = org.__dict__.copy()

            org_ins.pop('password', None)
            org_ins.pop('_state', None)
            org_ins.pop('created_at', None)
            org_ins.pop('updated_at', None)
            org_ins.pop('owner_email', None)

            org_ins['orgId'] = org_ins['id']
            org_ins.pop('id', None)
            all_org.append(org_ins)

        return all_org
    except Exception as exc:
        print(f'error retrieving all organiztions: {exc}')

def get_organzation(data: dict, orgId: str):
    """
    Retrieves all organzations
    """
    try:
        # retrieve the organisation using its provided orgId
        org = Organisation.objects.get(id=orgId)
        # return if no org found
        if not org:
            return {}

        # check if org found is owned by the user
        if org.owner_email == data.get('email'):
            # if owned by the user, sanitize and return the org
            return sanitize_organzations(org=org)

        # if not owned by the user, use the org to retrieve the users associated
        # with the org
        user_orgs = UserOrganisation.objects.filter(organisation=org)

        # retrieve the user object claiming the rights to see the organisation
        user = User.objects.get(id=data.get('user_id'))

        # iterate through the list of user_orgs returned
        for user_o in user_orgs:
            # check if the user is a member in one of the user_orgs and check
            # if the user_org the user is a member in is the same org the user is
            # looking to retrieve
            if user == user_o.user and org == user_o.organisation:
                # if there is a match, sanitize and return the org
                return sanitize_organzations(org=org)
        return {}
    except Exception as exc:
        print(f'error retrieving an organiztion: {exc}')


def add_organzation(data: dict, user_data: dict):
    """
    add an organzation
    """
    try:
        data["owner_email"] = user_data['email']
        org = Organisation.objects.create(**data)
        if org:
            return sanitize_organzations(org=org)
        else:
            return
    except Exception as exc:
        print(f'error retrieving all organiztions: {exc}')

def validate_data(data: dict):
    """
    Validates data
    """
    try:
        if len(data) < 2 or data.get('name').strip() == '' or not data.get('name'):
            return
        if data.get('description') and not isinstance(data.get('description'), str):
            return
        if "name" in data and "description" in data:
            if isinstance(data.get('name'), str):
                return escape_data(data)
            else:
                return
        else:
            return
    except Exception as exc:
        print(f'error retrieving all organiztions: {exc}')
