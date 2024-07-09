from django.test import TestCase
# from django.core.exceptions import PermissionDenied
from user.models import User
from organisation.models import Organisation
from user_organisation.models import UserOrganisation


class Test_User_Organisation_Creation(TestCase):
    """
    Test for integrated User, Organisation, and UserOrganisation creation.
    """
    def setUp(self) -> None:
        self.johnson_values = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "Johnson@gmail.com",
            "password": "johnson",
            "phone": "1234567890"
        }

        self.ben_values = {
            "firstName": "Ben",
            "lastName": "Dennis",
            "email": "Ben2@gmail.com",
            "password": "Ben",
            "phone": "1234567890"
        }

    def test_organisation_creation_from_user_creation(self):
        """
        Test for creating an Organisation object automatically upon User creation
        """
        johnson = User.objects.create(**self.johnson_values)

        johnson_org = Organisation.objects.get(owner_email=johnson.email)

        johnson_org = UserOrganisation.objects.get(user=johnson, organisation=johnson_org)

        self.assertTrue(johnson_org)
        self.assertTrue(johnson_org.role == 'owner')

    def test_member_cannot_delete_user_organisation(self):
        """

        """
        # create two users
        johnson = User.objects.create(**self.johnson_values)

        ben = User.objects.create(**self.ben_values)


        # retrieve johnson_org
        johnson_org = Organisation.objects.get(owner_email=johnson.email)

        # add ben to johnson_org
        ben_member_org = UserOrganisation.objects.create(user=ben,
                                                         organisation=johnson_org,
                                                         role="member")

        # try to delete user_organisation via ben
        error_message = f"Could not delete user_organisation, must be the owner to delete!: {ben_member_org.role}"
        with self.assertRaises(PermissionError, msg=error_message):
            ben_member_org.delete()
