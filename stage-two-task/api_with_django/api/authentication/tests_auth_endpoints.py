from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient


class Test_AUth_Endpoints(TestCase):
    """
    Tests for the AUTH API endpoints.
    """
    def setUp(self) -> None:
        """
        Setup for tests
        """
        self.client = APIClient()
        self.reg_user = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "Johnson@gmail.com",
            "password": "johnson",
            "phone": "1234567890"
        }

        self.reg_user2 = {
            "firstName": "",
            "lastName": "",
            "email": "",
            "password": "",
            "phone": "1234567890"
        }

        self.login_user1 = {
            "email": "Johnson@gmail.com",
            "password": "johnson",
        }

        self.login_user2 = {
            "email": "",
            "password": "",
        }

    def test_successful_user_registeration(self):
        """
        Test for successful user egistration.
        """
        url = reverse('register_user')

        res = self.client.post(url, self.reg_user, format='json')

        data: dict = res.json()

        self.assertTrue(res.status_code == 200)
        self.assertEqual(data.get('status'), "success")
        self.assertEqual(data.get('message'), "Registration successful")
        self.assertTrue(isinstance(data.get('data').get('accessToken'), str))
        self.assertTrue(isinstance(data.get('data').get('user'), dict))

        self.assertEqual(self.reg_user['firstName'], data.get('data').get('user').get('firstName'))
        self.assertEqual(self.reg_user['lastName'], data.get('data').get('user').get('lastName'))
        self.assertEqual(self.reg_user['email'], data.get('data').get('user').get('email'))
        self.assertEqual(self.reg_user['phone'], data.get('data').get('user').get('phone'))

        self.assertFalse(data.get('data').get('user').get('password'))


    def test_for_registration_validations(self):
        """
        Test for registration data validations
        """
        url = reverse('register_user')

        res = self.client.post(url, self.reg_user2, format='json')

        data: dict = res.json()

        self.assertTrue(res.status_code == 422)

        errors = data['errors']


        self.assertEqual(errors[0], {
                "firstName": '',
                "message": "firstName must not be empty or less than two characters",
            })
        self.assertEqual(errors[1], {
                "lastName": '',
                "message": "lastName must not be empty or less than two characters",
            })
        self.assertEqual(errors[2], {
                "email": '',
                "message": "An email address must have an @-sign.",
            })
        self.assertEqual(errors[3], {
                "password": '',
                "message": "password must not be empty or less than 6 chars.",
            })

    def test_for_unsuccessful_registration(self):
        """
        Test for unsuccessful registration.
        """
        url = reverse('register_user')

        res = self.client.post(url, data='bad json', content_type='text/html')
        data: dict = res.json()

        self.assertTrue(res.status_code == 400)
        self.assertEqual(data.get('status'), "Bad request")
        self.assertEqual(data.get('message'), "Registration unsuccessful")

    def test_for_logging_in_users(self):
        """
        Test for logging in a user
        """
        url2 = reverse('register_user')
        self.client.post(url2, self.reg_user, format='json')

        url = reverse('login_user')
        res = self.client.post(url, self.login_user1, format='json')

        data: dict = res.json()

        self.assertTrue(res.status_code == 200)
        self.assertEqual(data.get('status'), "success")
        self.assertEqual(data.get('message'), "Login successful")

        self.assertTrue(isinstance(data.get('data').get('accessToken'), str))
        self.assertTrue(isinstance(data.get('data').get('user'), dict))

        self.assertEqual(self.reg_user['firstName'], data.get('data').get('user').get('firstName'))
        self.assertEqual(self.reg_user['lastName'], data.get('data').get('user').get('lastName'))
        self.assertEqual(self.reg_user['email'], data.get('data').get('user').get('email'))
        self.assertEqual(self.reg_user['phone'], data.get('data').get('user').get('phone'))

        self.assertFalse(data.get('data').get('user').get('password'))

    def test_for_login_validations(self):
        """
        Test for login data validations
        """
        url = reverse('login_user')

        res = self.client.post(url, data=self.login_user2, format='json')
        data: dict = res.json()

        self.assertTrue(res.status_code == 401)
        self.assertEqual(data.get('status'), "Bad request")
        self.assertEqual(data.get('message'), "Authentication failed")
