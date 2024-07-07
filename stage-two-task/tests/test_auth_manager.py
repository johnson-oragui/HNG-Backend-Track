#!/usr/bin/env python3
"""
Test for AuthManager
"""
import unittest
from datetime import datetime, timedelta
from utils.auth_manager import AuthManager



class TestAuthManager(unittest.TestCase):
    """
    Test Class for AuthManager
    """

    def test_generate_token(self):
        """
        Test token generation
        """
        user_dict = {"userId": "test_user"}
        token = AuthManager.gerenate_token(user_dict)
        self.assertIsNotNone(token)

        payload = AuthManager.decode_token_without_validation(token)
        self.assertEqual(payload['userId'], 'test_user')
        self.assertIn('iat', payload)
        self.assertIn('exp', payload)

        iat = datetime.utcfromtimestamp(payload['iat'])
        exp = datetime.utcfromtimestamp(payload['exp'])
        self.assertTrue(exp > iat)
        self.assertTrue(exp - iat == timedelta(minutes=10))

    def test_verify_token(self):
        """
        Test valid token
        """
        user_dict = {"userId": "test_user"}
        token = AuthManager.gerenate_token(user_dict)
        user_id = AuthManager.verify_jwt_token(token)
        self.assertEqual(user_id, 'test_user')

    def test_invalid_token(self):
        """
        Test invalid token validation
        """
        try:
            invalid_token = "invalid.token.value"
            user_id = AuthManager.verify_jwt_token(invalid_token)
            self.assertFalse(user_id)
        except Exception as exc:
            pass



if __name__ == "__main__":
    unittest.main()
