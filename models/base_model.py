#!/usr/bin/python3

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base class for all models."""

    def __init__(self, *args, **kwargs):
        """Create a new instanc of BaseModel."""
        timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(
                            value, timestamp_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Updates the public instance attribute'updated_at'
        with the current datetime and save the model."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of dict instance.
        """
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["__class__"] = self.__class__.__name__
        return result

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
