#!/usr/bin/python3
"""file_storage.py module"""
import json


class FileStorage:
    """defined a class to serialize and
    deserialize json
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns returns the dictionary __objects
        """

        return FileStorage.__objects

    def new(self, obj):
        """
        public instance method that sets in __objects
        the obj with key <obj class name>.id

        Variables:
        ----------
        key [str] -- key format generated.
        """
        if obj:
            FileStorage.__objects[
                "{}.{}".format(obj.__class__.__name__, obj.id)
                ] = obj

    def save(self):
        """
        public instance method that serializes __objects
        to the JSON file (path: __file_path).

        Variables:
        ----------
        new_dict [dict] -- keys and values to build JSON.
        """
        my_dict = {}
        for key, value in FileStorage.__objects.items():
            my_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as files:
            json.dump(my_dict, files)

    def reload(self):
        """
        public instance method that deserializes a JSON
        file to __objects.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        try:
            with open(FileStorage.__file_path, mode='r') as files:
                my_dict = json.load(files)

            for key, value in my_dict.items():
                class_name = value.get('__class__')
                obj = eval(class_name + '(**value)')
                FileStorage.__objects[key] = obj

        except FileNotFoundError:
            pass
