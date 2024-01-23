#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import time
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = (
            datetime.strptime(kwargs["created_at"], str(time))
            if kwargs.get("created_at") and isinstance(kwargs["created_at"], str)
            else datetime.utcnow()
        )
        self.updated_at = (
            datetime.strptime(kwargs["updated_at"], str(time))
            if kwargs.get("updated_at") and isinstance(kwargs["updated_at"], str)
            else datetime.utcnow()
        )

        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        models.storage.save()

    def to_dict(self):
        """Converts instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary.pop('_sa_instance_state', None)
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
