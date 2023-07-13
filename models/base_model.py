#!/usr/bin/python3
"""base_model.py module"""
import uuid
from datetime import datetime
from models import storage


class BaseModel():
    """
    BaseModel class:
    ----------------
    It defines all common attributes/methods
    for the other classes.

    """

    def __init__(self, *args, **kwargs):
        """
        Object constructor.

        Attributes:
        ----------
        id [str] -- UUID generated with python uuid.
        created_at [datetime] -- contains datetime obj.
        updated_at [datetime] -- contains datetime obj.
        __class__ [str] -- BaseModel class.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at":
                    self.created_at = datetime.strptime(value,
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(value,
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    if key != "__class__":
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            # calling method new(self) on storage (task5).
            storage.new(self)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        mydict = self.__dict__.copy()
        mydict["created_at"] = self.created_at.isoformat()
        mydict["updated_at"] = self.updated_at.isoformat()
        mydict["__class__"] = self.__class__.__name__
        return mydict

    def __str__(self):
        """print str representation of the BaseModel instance."""
        return "[{}] ({}) {}".format(
                                self.__class__.__name__,
                                self.id, self.__dict__
                                )
