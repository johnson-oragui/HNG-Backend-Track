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

    def test_organisation_creation_from_user_creation(self):
        """
        Test for creating an Organisation object automatically upon User creation
        """
        new_user = User.objects.create(**self.user_values)

        new_org = Organisation.objects.get(owner_email=new_user.email)


        self.assertEqual(new_org.name, "Johnson's Organisation")
        self.assertEqual(new_org.description, "Johnson's Organisation is the Greatest")
        self.assertEqual(new_org.owner_email, "Johnson@gmail.com")


        new_user_org = UserOrganisation.objects.get(user=new_user)

        self.assertEqual(new_org, new_user_org.organisation)
        self.assertEqual(new_user, new_user_org.user)
