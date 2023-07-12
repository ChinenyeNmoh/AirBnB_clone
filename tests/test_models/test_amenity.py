#!/usr/bin/python3
"""Defines unittests for models/amenity.py.
Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_instanttype(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_values(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_type(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_type(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_type(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_properties(self):
        a1 = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", a1.__dict__)

    def test_unique_ids(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertNotEqual(a1.id, a2.id)

    def test_created_at(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.created_at, a2.created_at)

    def test_updated_at(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.updated_at, a2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "2468"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (2468)", amstr)
        self.assertIn("'id': '2468'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_str = dt.isoformat()
        a1 = Amenity(id="345", created_at=dt_str, updated_at=dt_str)
        self.assertEqual(a1.id, "345")
        self.assertEqual(a1.created_at, dt)
        self.assertEqual(a1.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

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
        a1 = Amenity()
        sleep(0.05)
        updated_at1 = a1.updated_at
        a1.save()
        self.assertLess(updated_at1, a1.updated_at)

    def test_two_saves(self):
        a1 = Amenity()
        sleep(0.05)
        first_updated_at = a1.updated_at
        a1.save()
        second_updated_at = a1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        a1.save()
        self.assertLess(second_updated_at, a1.updated_at)

    def test_save_with_arg(self):
        a1 = Amenity()
        with self.assertRaises(TypeError):
            a1.save(None)

    def test_save_updates_file(self):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_keys(self):
        a1 = Amenity()
        self.assertIn("id", a1.to_dict())
        self.assertIn("created_at", a1.to_dict())
        self.assertIn("updated_at", a1.to_dict())
        self.assertIn("__class__", a1.to_dict())

    def test_newattributes(self):
        a1 = Amenity()
        a1.name = "Chidi"
        a1.age = 8
        self.assertEqual("Chidi", a1.name)
        self.assertIn("age", a1.to_dict())

    def test_attributestypes(self):
        a1 = Amenity()
        a1_dict = a1.to_dict()
        self.assertEqual(str, type(a1_dict["id"]))
        self.assertEqual(str, type(a1_dict["created_at"]))
        self.assertEqual(str, type(a1_dict["updated_at"]))

    def test_to_dict_result(self):
        dt = datetime.today()
        a1 = Amenity()
        a1.id = "2468"
        a1.created_at = a1.updated_at = dt
        mydict = {
            'id': '2468',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(a1.to_dict(), mydict)

    def test_contrast_to_dict_dunder_dict(self):
        a1 = Amenity()
        self.assertNotEqual(a1.to_dict(), a1.__dict__)

    def test_to_dict_with_arg(self):
        a1 = Amenity()
        with self.assertRaises(TypeError):
            a1.to_dict(None)


if __name__ == "__main__":
    unittest.main()
