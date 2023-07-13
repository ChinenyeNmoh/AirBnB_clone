#!/usr/bin/python3
"""Module for test BaseModel class"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_class(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def teststorage(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_type(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_type(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_type(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_object_equality(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_created_at(self):
        b1 = BaseModel()
        sleep(0.10)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def test_updated_at(self):
        b1 = BaseModel()
        sleep(0.05)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        b1 = BaseModel(None)
        self.assertNotIn(None, b1.__dict__.values())

    def test_with_kwargs(self):
        dt = datetime.today()
        dt_str = dt.isoformat()
        b1 = BaseModel(id="267", created_at=dt_str, updated_at=dt_str)
        self.assertEqual(b1.id, "267")
        self.assertEqual(b1.created_at, dt)
        self.assertEqual(b1.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_str = dt.isoformat()
        b1 = BaseModel("12", id="267", created_at=dt_str, updated_at=dt_str)
        self.assertEqual(b1.id, "267")
        self.assertEqual(b1.created_at, dt)
        self.assertEqual(b1.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        b1 = BaseModel()
        sleep(0.05)
        updated_at1 = b1.updated_at
        b1.save()
        self.assertLess(updated_at1, b1.updated_at)

    def test_updatedsaves(self):
        b1 = BaseModel()
        sleep(0.05)
        updated_at1 = b1.updated_at
        b1.save()
        updated_at2 = b1.updated_at
        self.assertLess(updated_at1, updated_at2)
        sleep(0.05)
        b1.save()
        self.assertLess(updated_at1, b1.updated_at)

    def test_save_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dictkeys(self):
        b1 = BaseModel()
        self.assertIn("id", b1.to_dict())
        self.assertIn("created_at", b1.to_dict())
        self.assertIn("updated_at", b1.to_dict())
        self.assertIn("__class__", b1.to_dict())

    def test_added_attributes(self):
        b1 = BaseModel()
        b1.name = "Osinachi"
        b1.age = 98
        self.assertIn("name", b1.to_dict())
        self.assertIn("age", b1.to_dict())

    def test_strs_keys(self):
        b1 = BaseModel()
        b1_dict = b1.to_dict()
        self.assertEqual(str, type(b1_dict["created_at"]))
        self.assertEqual(str, type(b1_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        b1 = BaseModel()
        b1.id = "267665"
        b1.created_at = b1.updated_at = dt
        mydict = {
            'id': '267665',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(b1.to_dict(), mydict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
