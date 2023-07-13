#!/usr/bin/python3
""" Unittest for User class """
import unittest
import json
import pep8
import os
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):

    def setUp(self):
        """SetUp method"""
        self.user1 = User()
        self.user1.email = "chiumeh@alx.com"
        self.user1.password = "aeiou123452676"
        self.user1.first_name = "Nenye"
        self.user1.last_name = "Umeaku"

    def test_base_pep8(self):
        """Test for pep8"""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['./models/user.py'])
        self.assertEqual(result.total_errors, 1)

    def test_is_instance(self):
        """Test for instantiation"""
        self.assertIsInstance(self.user1, User)

    def test_attributes(self):
        """Test to check attributes"""
        self.user1.save()
        user1_json = self.user1.to_dict()
        my_new_user = User(**user1_json)
        self.assertEqual(my_new_user.id, self.user1.id)
        self.assertEqual(my_new_user.created_at, self.user1.created_at)
        self.assertEqual(my_new_user.updated_at, self.user1.updated_at)
        self.assertIsNot(self.user1, my_new_user)

    def test_subclass(self):
        """Test to check the inheritance"""
        self.assertTrue(issubclass(self.user1.__class__, BaseModel), True)

    def test_save(self):
        """Test to check save method"""
        variable_update = self.user1.updated_at
        self.user1.save()
        self.assertNotEqual(variable_update, self.user1.updated_at)
