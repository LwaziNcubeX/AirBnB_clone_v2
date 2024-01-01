#!/usr/bin/python3
""" State Module for HBNB project """
import os

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

    if HBNB_TYPE_STORAGE == 'db':
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances"""
            all_cities = models.storage.all("City")
            state_cities = [city for city in all_cities.values() if city.state_id == self.id]
            return state_cities

    def __init__(self, *args, **kwargs):
        """Instantiates a new State"""
        super().__init__(*args, **kwargs)
