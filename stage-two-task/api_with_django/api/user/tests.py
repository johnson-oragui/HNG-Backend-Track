from django.test import TestCase
from user.models import User
from organisation.models import Organisation
from user_organisation.models import UserOrganisation


class TestIntegrateModels(TestCase):
    """
    Test for integrated User, Organisation, and UserOrganisation creation.
    """
    def setUp(self) -> None:
        self.user_values = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "Johnson@gmail.com",
            "password": "johnson",
            "phone": "1234567890"
        }

    def test_user_creation(self):
        """
        Test for creating a User object with specified values.
        """
        new_user = User.objects.create(**self.user_values)
        print('new_user: ', new_user)

        self.assertEqual(new_user.firstName, self.user_values["firstName"])
        self.assertEqual(new_user.lastName, self.user_values["lastName"])
        self.assertEqual(new_user.email, self.user_values["email"])
        self.assertTrue(new_user.password)
        self.assertEqual(new_user.phone, self.user_values["phone"])

    def test_organisation_creation_from_user_creation(self):
        """
        Test for creating an Organisation object automatically upon User creation
        """
        new_user = User.objects.create(**self.user_values)

        new_org = Organisation.objects.get(owner_email=new_user.email)

        print('new_org: ', new_org)

        self.assertEqual(new_org.name, "Johnson's Organisation")
        self.assertEqual(new_org.description, "Johnson's Organisation is the Greatest")
        self.assertEqual(new_org.owner_email, "Johnson@gmail.com")

    def test_user_organisation_creation(self):
        """
        Test for auto creation of user_organisation fron user creation
        """
        new_user = User.objects.create(**self.user_values)

        new_user_org = UserOrganisation.objects.get(user=new_user)
        print('new_user_org: ', new_user_org)

        self.assertEqual(new_user_org.role, "owner")
