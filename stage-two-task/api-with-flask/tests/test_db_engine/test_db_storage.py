#!/usr/bin/env python3
"""
Test for DBSTorage
"""
import unittest
from datetime import datetime, timedelta
from utils.auth_manager import AuthManager
from models import DBStorage
from models.user import User
from models.organisation import Organisation

class TestOrganisationAccess(unittest.TestCase):

    def setUp(self):
        # Set up test data and session
        self.session = DBStorage().sess()
        self.user1 = User(userId='user1', firstName='Test', lastName='User', email='test1@example.com', password='password')
        self.user2 = User(userId='user2', firstName='Test', lastName='User', email='test2@example.com', password='password')
        self.org1 = Organisation(orgId='org1', name="User1's Organisation", description='')
        self.org2 = Organisation(orgId='org2', name="User2's Organisation", description='')
        self.session.add_all([self.user1, self.user2, self.org1, self.org2])
        self.session.commit()

    def tearDown(self):
        # Clean up the test session
        self.session.rollback()
        self.session.close()

    def test_user_access_to_own_organisation(self):
        # token = AuthManager.gerenate_token({"userId": self.user1.userId})
        # Logic to check user1 can access org1
        pass

    def test_user_cannot_access_other_organisation(self):
        # token = AuthManager.gerenate_token({"userId": self.user1.userId})
        # Logic to check user1 cannot access org2
        pass
