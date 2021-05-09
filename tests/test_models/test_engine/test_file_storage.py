#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import uuid
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)
        self.assertGreater(len(new_dict), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload(self):
        """Test that objects are properly reloaded."""
        fs = FileStorage()
        inst1 = BaseModel()
        fs.new(inst1)
        fs.save()
        time = inst1.created_at
        fs.reload()
        for value in fs.all().values():
            if inst1 == value:
                self.assertEqual(value.created_at, time)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test delete method of FileStorage."""
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        state_id = new_state.id
        fs.save()
        fs.delete(new_state)
        fs.save()
        with open("file.json", encoding="UTF-8") as fd:
            state_dict = json.load(fd)
        for keys in state_dict.keys():
            new_key = keys.split('.')[1]
            self.assertNotEqual(state_id, new_key)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_close(self):
        """Test correct call of the reload method."""
        fs = FileStorage()
        inst1 = BaseModel()
        fs.new(inst1)
        fs.save()
        time = inst1.created_at
        fs.reload()
        for value in fs.all().values():
            if inst1 == value:
                self.assertEqual(value.created_at, time)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get method retrieves the correct object."""
        # Test correct ID
        fs = FileStorage()
        inst1 = State()
        inst1.name = "Alabama"
        fs.new(inst1)
        new_id = inst1.id
        fs.save()
        state = fs.get("State", new_id)
        self.assertEqual(state.name, "Alabama")
        # Test incorrect class
        inst2 = State()
        fs.new(inst2)
        new_id = inst2.id
        fs.save()
        ret = fs.get(Amenity, new_id)
        self.assertEqual(ret, None)
        # Test non-existant ID
        new_id = str(uuid.uuid4())
        ret = fs.get(State, new_id)
        self.assertEqual(ret, None)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count method returns the correct count."""
        # Test with class parameter
        fs = FileStorage()
        old_count = fs.count(State)
        new = State(name="Alabama")
        fs.new(new)
        fs.save()
        new_count = fs.count(State)
        self.assertEqual(old_count + 1, new_count)
        # Test without class parameter
        old_count = fs.count()
        new = State(name="Michigan")
        fs.new(new)
        fs.save()
        new_count = fs.count()
        self.assertEqual(old_count + 1, new_count)
