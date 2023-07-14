#!/usr/bin/python3
""" Unittest for FileStorage class """
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_type(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_filepath(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

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
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        b1 = BaseModel()
        u1 = User()
        s1 = State()
        pl = Place()
        c1 = City()
        a1 = Amenity()
        r1 = Review()
        models.storage.new(b1)
        models.storage.new(u1)
        models.storage.new(s1)
        models.storage.new(pl)
        models.storage.new(c1)
        models.storage.new(a1)
        models.storage.new(r1)
        self.assertIn("BaseModel." + b1.id, models.storage.all().keys())
        self.assertIn(b1, models.storage.all().values())
        self.assertIn("User." + u1.id, models.storage.all().keys())
        self.assertIn(u1, models.storage.all().values())
        self.assertIn("State." + s1.id, models.storage.all().keys())
        self.assertIn(s1, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + c1.id, models.storage.all().keys())
        self.assertIn(c1, models.storage.all().values())
        self.assertIn("Amenity." + a1.id, models.storage.all().keys())
        self.assertIn(a1, models.storage.all().values())
        self.assertIn("Review." + r1.id, models.storage.all().keys())
        self.assertIn(r1, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        b1 = BaseModel()
        u1 = User()
        s1 = State()
        pl = Place()
        c1 = City()
        a1 = Amenity()
        r1 = Review()
        models.storage.new(b1)
        models.storage.new(u1)
        models.storage.new(s1)
        models.storage.new(pl)
        models.storage.new(c1)
        models.storage.new(a1)
        models.storage.new(r1)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + b1.id, save_text)
            self.assertIn("User." + u1.id, save_text)
            self.assertIn("State." + s1.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + c1.id, save_text)
            self.assertIn("Amenity." + a1.id, save_text)
            self.assertIn("Review." + r1.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        b1 = BaseModel()
        u1 = User()
        s1 = State()
        pl = Place()
        c1 = City()
        a1 = Amenity()
        r1 = Review()
        models.storage.new(b1)
        models.storage.new(u1)
        models.storage.new(s1)
        models.storage.new(pl)
        models.storage.new(c1)
        models.storage.new(a1)
        models.storage.new(r1)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b1.id, objs)
        self.assertIn("User." + u1.id, objs)
        self.assertIn("State." + s1.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + c1.id, objs)
        self.assertIn("Amenity." + a1.id, objs)
        self.assertIn("Review." + r1.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
