#!/usr/bin/python3
""" Unittest for User class """
import datetime
import unittest
from models.base_model import BaseModel
from models.user import User


class TestUserModel(unittest.TestCase):
    """test class for testing user models
    """
    def setUp(self):
        self.temp_b = User()

    def tearDown(self):
        self.temp_b = None

    def test_type(self):
        """type checks for user model
        """
        self.assertEqual(issubclass(self.temp_b.__class__, BaseModel), True)
        self.assertEqual(isinstance(self.temp_b, BaseModel), True)
        self.assertEqual(isinstance(self.temp_b, User), True)
        self.assertEqual(type(self.temp_b), User)

    def test_basic_attribute_set(self):
        """basic attribute assignment tests for user model
        """
        self.temp_b.name = "Ifeoma"
        self.temp_b.no = 30
        self.assertEqual(self.temp_b.name, "Ifeoma")
        self.assertEqual(self.temp_b.no, 30)

    def test_emailtype(self):
        """tests the email type of user
        """
        self.assertEqual(type(User.email), str)

    def test_passwordtype(self):
        """tests the password type of user
        """
        self.assertEqual(type(User.password), str)

    def test_first_nametype(self):
        """tests the first_name type of user
        """
        self.assertEqual(type(User.first_name), str)

    def test_last_nametype(self):
        """tests the last_name type of user
        """
        self.assertEqual(type(User.last_name), str)

    def test_string_return(self):
        """tests the string method to make sure it returns
            the proper string
        """
        my_str = str(self.temp_b)
        id_test = "[User] ({})".format(self.temp_b.id)
        boolean = id_test in my_str
        self.assertEqual(True, boolean)
        boolean = "updated_at" in my_str
        self.assertEqual(True, boolean)
        boolean = "created_at" in my_str
        self.assertEqual(True, boolean)
        boolean = "datetime.datetime" in my_str
        self.assertEqual(True, boolean)

    def test_to_dict(self):
        """tests the to_dict method to make sure properly working
        """
        my_dict = self.temp_b.to_dict()
        self.assertEqual(str, type(my_dict['created_at']))
        self.assertEqual(my_dict['created_at'],
                         self.temp_b.created_at.isoformat())
        self.assertEqual(datetime.datetime, type(self.temp_b.created_at))
        self.assertEqual(my_dict['__class__'],
                         self.temp_b.__class__.__name__)
        self.assertEqual(my_dict['id'], self.temp_b.id)

    def test_from_dict_class_attributes(self):
        """tests the from_dict method
        """
        my_dict = self.temp_b.to_dict()
        my_base = User(**my_dict)
        self.assertEqual(my_base.id, self.temp_b.id)
        self.assertEqual(my_base.updated_at, self.temp_b.updated_at)
        self.assertEqual(my_base.created_at, self.temp_b.created_at)
        self.assertEqual(my_base.__class__.__name__,
                         self.temp_b.__class__.__name__)

    def test_from_dictmethod(self):
        """tests from dict method of user class
        """
        self.temp_b.school = "Vilac"
        self.temp_b.age = 11
        my_dict = self.temp_b.to_dict()
        self.assertEqual(my_dict['age'], 11)
        my_base = BaseModel(**my_dict)
        self.assertEqual(my_base.age, self.temp_b.age)
        self.assertEqual(my_base.school, self.temp_b.school)
        self.assertEqual(my_base.created_at, self.temp_b.created_at)
