#!/usr/bin/env python3
"""
Unittest for API
"""
import os
import dotenv
import requests
import unittest
from models import DBStorage

dotenv.load_dotenv()


BASE_URL = "http://localhost:5000"


class TestRegisterEndpoint(unittest.TestCase):
    """
    CLass Test for Register endpoint
    """
    accessToken = ''
    orgId = ''
    userId = ''

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup for test
        """
        # os.environ['TEST'] = 'TEST'
        # test_value = os.getenv('TEST')
        # print(f"Current value of TEST: {test_value}")
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Teardown for tests
        """
        try:
            session = DBStorage()
            session.delete_data(all=True)
        except Exception as exc:
            print(f'an error occured during teardown: {exc}')
        # os.environ['TEST'] = 'NOT_TEST'
        # test_value = os.getenv('TEST')
        # print(f"Current value of TEST: {test_value}")

    def test_a_successful_registration(self):
        """
        Tests for successfull user registration
        """
        payload = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "johnson@gmail.com",
            "password": "password",
            "phone": "1234567890"
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)
        try:
            data = response.json()
        except ValueError as exc:
            print(f'error occured: {exc}')
        # print('data: ', data)

        self.assertEqual(data['status'], 'success')
        self.assertEqual(data["message"], "Registration successful")
        self.assertTrue(len(data["data"]) == 2)
        self.assertIn('accessToken', data['data'])
        self.assertIn('user', data['data'])
        self.assertIn('userId', data['data']['user'])
        self.assertEqual(data['data']['user']['firstName'], 'Johnson')
        self.assertEqual(data['data']['user']['lastName'], 'Dennis')
        self.assertEqual(data['data']['user']['email'], "johnson@gmail.com")
        self.assertFalse('password' in data['data']['user'])
        self.assertEqual(data['data']['user']['phone'], '1234567890')

        self.__class__.userId = data['data']['user']['userId']
        self.__class__.accessToken = data['data']['accessToken']


    def test_b_successful_organisation_creation(self):
        """
        Test that organisation was created with the user's firstName.
        """
        user_generated_organisation = "Johnson's Organisation"
        headers = {
            "Authorization": f"Bearer {self.__class__.accessToken}"
        }

        response2 = requests.get(f"{BASE_URL}/api/organisations", headers=headers)

        data2 = response2.json()

        # print('data2: ', data2)

        self.__class__.orgId = data2['data']['organisations'][0]['orgId']

        self.assertTrue(data2['status'] == "success")
        self.assertTrue(data2['message'] == "Successful")
        self.assertTrue(isinstance(data2['data']['organisations'][0]['orgId'], str))
        self.assertEqual(
            data2['data']['organisations'][0]['name'],
            user_generated_organisation
            )
        self.assertTrue(data2['data']['organisations'][0]['description'])
        self.assertEqual(data2['data']['organisations'][0]['description'], "Johnson's Organisation is One of a Kind.")


    def test_c_registration_validation_error(self):
        """
        Test for registration validation errors
        """
        payload = {
            "firstName": "",
            "lastName": "",
            "email": "",
            "password": "",
            "phone": "1234567890"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        self.assertEqual(response.status_code, 422)

        data = response.json()

        # print('error data: ', data)

        self.assertEqual(data['error'][0]['firstName'], '')
        self.assertEqual(data['error'][0]['message'], 'firstName must not be empty')

        self.assertEqual(data['error'][1]['lastName'], '')
        self.assertEqual(data['error'][1]['message'], 'lastName must not be empty')

        self.assertEqual(data['error'][2]['email'], '')
        self.assertEqual(data['error'][2]['message'], 'An email address must have an @-sign.')

        self.assertEqual(data['error'][3]['password'], '')
        self.assertEqual(data['error'][3]['message'], 'password must not be empty')

    def test_d_duplicate_email_and_error_status_code(self):
        """
        Test for duplicate user email during registration
        """
        payload = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "johnson@gmail.com",
            "password": "password",
            "phone": "1234567890"
        }

        expected_error_data = {
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
        }

        response1 = requests.post(f"{BASE_URL}/auth/register", json=payload)
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data, expected_error_data)



class TestLoginEndpoint(unittest.TestCase):
    """
    Test Class for Login
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup for Login
        """
        try:
            pass
        except Exception as exc:
            print(f'error occured in set up {exc}')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Teardown for tests
        """
        try:
            session = DBStorage()
            session.delete_data(all=True)
        except Exception as exc:
            print(f'an error occured during teardown: {exc}')
            pass

    def test_successful_login(self):
        """
        Test for successfult login
        """
        payload1 = {
            "firstName": "Johnson",
            "lastName": "Dennis",
            "email": "johnson@gmail.com",
            "password": "password",
            "phone": "1234567890"
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload1)


        payload = {
            "email": "johnson@gmail.com",
            "password": "password"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(response.status_code, 200)

        try:
            data = response.json()
        except ValueError as exc:
            print(f'error occured: {exc}')
        # print('data: ', data)

        self.assertEqual(data['status'], 'success')
        self.assertEqual(data["message"], "Login successful")
        self.assertTrue(isinstance(data['data'], dict) and len(data['data']) == 2)
        self.assertIn('accessToken', data['data'])
        self.assertTrue(data['data']['accessToken'] != None)
        self.assertEqual(data['data']['user']['firstName'], payload1['firstName'])
        self.assertEqual(data['data']['user']['lastName'], payload1['lastName'])

        self.assertEqual(data['data']['user']['email'], payload['email'])

        self.assertEqual(data['data']['user']['phone'], payload1['phone'])

    def test_unsuccessful_login(self):
        """
        Test for unsuccessful login
        """
        payload = {
            "email": "johnson@gmail.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(response.status_code, 401)
        data = response.json()
        # print('data: ', data)
        self.assertEqual(data['status'], "Bad request")
        self.assertEqual(data['message'], 'Authentication failed')
        self.assertEqual(data['statusCode'], 401)

        payload2 = {
            "email": "wrong@gmail.com",
            "password": "password"
        }

        response2 = requests.post(f"{BASE_URL}/auth/login", json=payload2)
        self.assertEqual(response2.status_code, 401)
        data = response2.json()
        self.assertEqual(data['status'], "Bad request")
        self.assertEqual(data['message'], 'Authentication failed')
        self.assertEqual(data['statusCode'], 401)


class TestUsersOrganisationsEndpoint(unittest.TestCase):
    """
    Test Class for Login
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup for Login
        """
        try:
            cls.payload = {
                "firstName": "John",
                "lastName": "Dennis",
                "email": "john@gmail.com",
                "password": "password",
                "phone": "1234567890"
            }

            cls.res = requests.post(f"{BASE_URL}/auth/register", json=cls.payload)
            try:
                cls.data = cls.res.json()
                cls.accessToken = cls.data["data"]["accessToken"]
                cls.orgId = None
                cls.userId = cls.data['data']['user']['userId']
            except ValueError as exc:
                print(f'error occured: {exc}')
            # print('data: ', cls.data)
        except Exception as exc:
            print(f'error occured in set up {exc}')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Teardown for tests
        """
        try:
            session = DBStorage()
            session.delete_data(all=True)
        except Exception as exc:
            print(f'an error occured during teardown: {exc}')

    def test_a_users_endpoint_with_id(self):
        """
        Test for successful login
        """
        userId = self.__class__.data['data']["user"]['userId']
        accessToken = self.__class__.accessToken

        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        response = requests.get(f"{BASE_URL}/api/users/{userId}", headers=headers)

        self.assertEqual(response.status_code, 200)

        try:
            data = response.json()
        except ValueError as exc:
            print(f"{exc}")
        # print("test data: ", data)

        self.assertEqual(data['status'], 'success')
        self.assertEqual(data["message"], "Successful")

        self.assertEqual(data['data']['userId'], userId)
        self.assertEqual(data['data']['firstName'], self.__class__.payload["firstName"])
        self.assertEqual(data['data']['lastName'], self.__class__.payload["lastName"])

        self.assertEqual(data['data']['email'], self.__class__.payload["email"])

        self.assertEqual(data['data']['phone'], self.__class__.payload["phone"])

    def test_all_organisations_endpoint(self):
        """
        Test for retrieving all organisatons related to a user
        """
        accessToken = self.__class__.accessToken

        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        response = requests.get(f"{BASE_URL}/api/organisations", headers=headers)

        self.assertEqual(response.status_code, 200)

        try:
            data = response.json()
        except ValueError as exc:
            print(f"{exc}")

        self.__class__.orgId = data["data"]["organisations"][0]["orgId"]

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful")

        self.assertIn("orgId", data["data"]["organisations"][0])

        self.assertEqual(data["data"]["organisations"][0]["name"], "John's Organisation")

        self.assertEqual(data["data"]["organisations"][0]["description"], "John's Organisation is One of a Kind.")

    def test_get_single_organisation_endpoint(self):
        """
        Test for retrieving a single organisation for a user
        """
        accessToken = self.__class__.accessToken
        orgId = self.__class__.orgId

        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        response = requests.get(f"{BASE_URL}/api/organisations/{orgId}", headers=headers)

        self.assertEqual(response.status_code, 200)

        try:
            data = response.json()
        except ValueError as exc:
            print(f"{exc}")

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Successful")

        self.assertTrue(data["data"]["orgId"] == orgId)

        self.assertEqual(data["data"]["name"], "John's Organisation")

        self.assertEqual(data["data"]["description"], "John's Organisation is One of a Kind.")

    def test_p_organisation_creation_endpoint(self):
        """
        Test for creating new organisation
        """
        accessToken = self.__class__.accessToken

        payload = {
            "name": "John's Organisation of Winners",
            "description": "All We do is WIn! WIn!! WIn!!!"
        }

        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        response = requests.post(f"{BASE_URL}/api/organisations", json=payload, headers=headers)
        # print('data: ', response.json())
        self.assertEqual(response.status_code, 201)

        try:
            data = response.json()
        except ValueError as exc:
            print(f"{exc}")

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Organisation created successfully")

        self.assertTrue(data["data"]["orgId"])

        self.assertEqual(data["data"]["name"], "John's Organisation of Winners")

        self.assertEqual(data["data"]["description"], "All We do is WIn! WIn!! WIn!!!")

        payload2 = {
            "name": "",
            "description": "All We do is WIn! WIn!! WIn!!!"
        }

        response2 = requests.post(f"{BASE_URL}/api/organisations", data=payload2, headers=headers)

        self.assertEqual(response2.status_code, 400)
        # print('data: ', response2.json())

        try:
            data = response2.json()
        except ValueError as exc:
            print(f"{exc}")

        self.assertEqual(data["status"], "Bad Request")
        self.assertEqual(data["message"], "Client error")
        self.assertEqual(data["statusCode"], 400)

    def test_z_add_user_to_organisation_endpoint(self):
        """
        Test for adding a user to organisation
        """
        #create a new user to add to organisation

        new_payload = {
                "firstName": "Benson",
                "lastName": "Dennis",
                "email": "Benson@gmail.com",
                "password": "password",
                "phone": "1234567890"
            }

        expected_response = {
            "status": "success",
            "message": "User added to organisation successfully"
        }

        # adding a new user
        new_res = requests.post(f"{BASE_URL}/auth/register", json=new_payload)
        try:
            new_data = new_res.json()
            new_userId = new_data['data']['user']['userId']
        except ValueError as exc:
            print(f'error occured: {exc}')

        # add new user to organisation

        accessToken = self.__class__.accessToken

        headers = {
            "Authorization": f"Bearer {accessToken}"
        }

        payload2 = {
            "userId": new_userId  # userId of user to add to organisation
        }

        # userId of organisation owner
        orgId = self.__class__.orgId

        # adding the new user to an organisation
        response = requests.post(f"{BASE_URL}/api/organisations/{orgId}/users", json=payload2, headers=headers)
        # print('data: ', response.json())
        self.assertEqual(response.status_code, 200)

        try:
            data = response.json()
        except ValueError as exc:
            print(f"{exc}")

        self.assertEqual(data, expected_response)



if __name__ == '__main__':
    unittest.main()
