#!/usr/bin/python3
"""Module for test City class"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_attribute(self):
        c1 = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(c1))
        self.assertNotIn("state_id", c1.__dict__)

    def test_name_attribute(self):
        c1 = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(c1))
        self.assertNotIn("name", c1.__dict__)

    def test_unique_ids(self):
        c1 = City()
        c2 = City()
        self.assertNotEqual(c1.id, c2.id)

    def test_created_at(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.created_at, c2.created_at)

    def test_updated_at(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.updated_at, c2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        c1 = City(None)
        self.assertNotIn(None, c1.__dict__.values())

    def test_kwargs(self):
        dt = datetime.today()
        dt_str = dt.isoformat()
        c1 = City(id="334", created_at=dt_str, updated_at=dt_str)
        self.assertEqual(c1.id, "334")
        self.assertEqual(c1.created_at, dt)
        self.assertEqual(c1.updated_at, dt)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        c1 = City()
        sleep(0.05)
        first_updated_at = c1.updated_at
        c1.save()
        self.assertLess(first_updated_at, c1.updated_at)

    def test_two_saves(self):
        c1 = City()
        sleep(0.05)
        first_updated_at = c1.updated_at
        c1.save()
        second_updated_at = c1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        c1.save()
        self.assertLess(second_updated_at, c1.updated_at)

    def test_save_with_arg(self):
        c1 = City()
        with self.assertRaises(TypeError):
            c1.save(None)

    def test_save_updates_file(self):
        c1 = City()
        c1.save()
        c1id = "City." + c1.id
        with open("file.json", "r") as f:
            self.assertIn(c1id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_keys(self):
        c1 = City()
        self.assertIn("id", c1.to_dict())
        self.assertIn("created_at", c1.to_dict())
        self.assertIn("updated_at", c1.to_dict())
        self.assertIn("__class__", c1.to_dict())

    def test_newattributes(self):
        c1 = City()
        c1.name = "Chinedu"
        c1.age = 6
        self.assertEqual("Chinedu", c1.name)
        self.assertIn("age", c1.to_dict())

    def test_attributestypes(self):
        c1 = City()
        c1_dict = c1.to_dict()
        self.assertEqual(str, type(c1_dict["id"]))
        self.assertEqual(str, type(c1_dict["created_at"]))
        self.assertEqual(str, type(c1_dict["updated_at"]))

    def test_to_dict_result(self):
        dt = datetime.today()
        c1 = City()
        c1.id = "2468"
        c1.created_at = c1.updated_at = dt
        mydict = {
            'id': '2468',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(c1.to_dict(), mydict)

    def test_contrast_to_dict_dunder_dict(self):
        c1 = City()
        self.assertNotEqual(c1.to_dict(), c1.__dict__)

    def test_to_dict_with_None(self):
        c1 = City()
        with self.assertRaises(TypeError):
            c1.to_dict(None)


if __name__ == "__main__":
    unittest.main()
