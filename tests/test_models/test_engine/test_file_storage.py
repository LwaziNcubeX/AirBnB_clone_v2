#!/usr/bin/python3
""" Module for testing file storage"""
import unittest

import models
from models.base_model import BaseModel
from models import storage
import os


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_create_with_params(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.onecmd('create State name="California" number_rooms=2')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.onecmd('create Place name="My little house" price_by_night=300 '
                        'latitude=37.773972 longitude=-122.431297')
            place_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.onecmd('create Place name="My other house" bad_param=123')
            new_place_id = f.getvalue().strip()

        # Check that the objects were actually created
        self.assertIsNotNone(models.storage.get('State', state_id))
        self.assertIsNotNone(models.storage.get('Place', place_id))
        self.assertIsNotNone(models.storage.get('Place', new_place_id))

        # Check that the objects have the correct attributes
        state = models.storage.get('State', state_id)
        self.assertEqual(state.name, 'California')
        self.assertEqual(state.number_rooms, 2)

        place = models.storage.get('Place', place_id)
        self.assertEqual(place.name, 'My little house')
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

        new_place = models.storage.get('Place', new_place_id)
        self.assertEqual(new_place.name, 'My other house')
        self.assertIsNone(new_place.bad_param)
