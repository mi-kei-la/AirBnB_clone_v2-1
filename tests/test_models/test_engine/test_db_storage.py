#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = DBStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._DBStorage__objects)
        self.assertGreater(len(new_dict), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_with_class(self):
        """Test that all returns all rows of a certain class."""
        storage = DBStorage()
        all_states = storage.all(State)
        for dict_obj in all_states.values():
            self.assertIsInstance(dict_obj, State)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        storage = DBStorage()
        old_all = storage.all()
        new_state = State()
        new_state.name = "Puerto Rico"
        new_state_id = new_state.id
        self.assertNotIn(new_state, old_all.values())
        storage.new(new_state)
        storage.save()
        new_all = storage.all()
        self.assertNotEqual(len(old_all), len(new_all))
        self.assertIn(new_state, new_all.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = DBStorage()
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for k, v in result.items():
            temp_list.append(k.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test that delete properly removes an object."""
        storage = DBStorage()
        new_user = User(email="haha@hehe.com", password="abc",
                        first_name="Jhon", last_name="Wick")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """Test that reload correctly reloads data from db."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_close(self):
        """Test that the current session is correctly closed."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves the correct object."""
        # Test correct ID
        db = DBStorage()
        inst1 = State()
        inst1.name = "Alabama"
        db.new(inst1)
        new_id = inst1.id
        db.save()
        state = db.get("State", new_id)
        self.assertEqual(state.name, "Alabama")
        # Test incorrect class
        inst2 = State()
        db.new(inst2)
        new_id = inst2.id
        db.save()
        ret = db.get(Amenity, new_id)
        self.assertEqual(ret, None)
        # Test non-existant ID
        new_id = str(uuid.uuid4())
        ret = db.get(State, new_id)
        self.assertEqual(ret, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct number of objects."""
        # Test with class parameter
        db = DBStorage()
        old_count = db.count(State)
        new = State(name="Alabama")
        db.new(new)
        db.save()
        new_count = db.count(State)
        self.assertEqual(old_count + 1, new_count)
        # Test without class parameter
        old_count = db.count()
        new = State(name="Michigan")
        db.new(new)
        db.save()
        new_count = db.count()
        self.assertEqual(old_count + 1, new_count)
