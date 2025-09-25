import unittest
from unittest.mock import MagicMock, Mock, patch

from library import library_db_interface;
from library.patron import Patron
import os

class TestLibraryDB_API(unittest.TestCase):
    
    def setUp(self):
        # make mocks
        self.lib_db = library_db_interface.Library_DB()
        #avoids making real files during runs
        self.test_db_file = 'test_db.json'
    
    @patch('library.library_db_interface.TinyDB')
    def test_insert_patron_success(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        #Mock success
        mock_db_instance.insert.return_value = 1

        #Does not exist, but should exist after insert
        lib_db = library_db_interface.Library_DB()
        lib_db.retrieve_patron = MagicMock(return_value=None)
        
        patron = Patron("John", "Doe", 25, "P001")

        result = lib_db.insert_patron(patron)

        self.assertEqual(result, 1)
        mock_db_instance.insert.assert_called_once()
    
    @patch('library.library_db_interface.TinyDB')
    def test_insert_not_patron(self, mock_tinydb):
        lib_db = library_db_interface.Library_DB()
        invalid_patron = None

        result = lib_db.insert_patron(invalid_patron)
        self.assertIsNone(result)

    @patch('library.library_db_interface.TinyDB')
    def test_update_patron_success(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        lib_db = library_db_interface.Library_DB()

        patron = Patron("John", "Doe", 25, "P001")
        lib_db.update_patron(patron)

        mock_db_instance.update.assert_called_once()

    @patch('library.library_db_interface.TinyDB')
    def test_update_patron_invalid(self, mock_tinydb):
        lib_db = library_db_interface.Library_DB()
        result = lib_db.update_patron(None)
        self.assertIsNone(result)
    
    @patch('library.library_db_interface.TinyDB')
    def test_insert_copy_patron(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance

        lib_db = library_db_interface.Library_DB()
        patron = Patron("John", "Doe", 25, "P001")

        #Mock into returning the patron we just made (a dupe!)
        lib_db.retrieve_patron = MagicMock(return_value=patron)

        result = lib_db.insert_patron(patron)

        self.assertIsNone(result)
        mock_db_instance.insert.assert_not_called()
    
    @patch('library.library_db_interface.TinyDB')
    def test_get_patron_count(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        mock_db_instance.all.return_value = [
            {'fname': 'John', 'lname': 'Doe', 'age': 25, 'memberID': 'P001'},
            {'fname': 'Jane', 'lname': 'Doe', 'age': 23, 'memberID': 'P002'}
        ]
        
        lib_db = library_db_interface.Library_DB()
        result = lib_db.get_patron_count()
        self.assertEqual(result, 2)
        mock_db_instance.all.assert_called_once()

    
    @patch('library.library_db_interface.TinyDB')
    def test_retrieve_patron_success(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        
        #successful/expected result
        mock_db_instance.search.return_value = [
            {'fname': 'John', 'lname': 'Doe', 'age': 25, 'memberID': 'P001', 'borrowed_books': []}
        ]
        
        lib_db = library_db_interface.Library_DB()
        result = lib_db.retrieve_patron("P001")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Patron)
        self.assertEqual(result.get_memberID(), "P001")
        self.assertEqual(result.get_fname(), "John")
        self.assertEqual(result.get_lname(), "Doe")
        self.assertEqual(result.get_age(), 25)
        mock_db_instance.search.assert_called_once()
    
    @patch('library.library_db_interface.TinyDB')
    def test_retrieve_patron_invalid(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        
        #Mock empty (not found)
        mock_db_instance.search.return_value = []
        
        lib_db = library_db_interface.Library_DB()
        result = lib_db.retrieve_patron("INVALID_ID")
        self.assertIsNone(result)
        mock_db_instance.search.assert_called_once()
    
    @patch('library.library_db_interface.TinyDB')
    def test_retrieve_patron_insert_duplicate_id_first(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance

        #First I add two patrons with the same ID
        mock_db_instance.search.return_value = [
            {'fname': 'John', 'lname': 'Doe', 'age': 25, 'memberID': 'P001', 'borrowed_books': []},
            {'fname': 'Jane', 'lname': 'Smith', 'age': 30, 'memberID': 'P001', 'borrowed_books': []}  # Duplicate ID
        ]
        
        lib_db = library_db_interface.Library_DB()
        
        #Then I check to see what happens when I ask for the result
        result = lib_db.retrieve_patron("P001")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Patron)
        self.assertEqual(result.get_memberID(), "P001")
        self.assertEqual(result.get_fname(), "John")
        self.assertEqual(result.get_lname(), "Doe")
        self.assertEqual(result.get_age(), 25)
        mock_db_instance.search.assert_called_once()

    #This is the same test as above, I just check to see if any other info comes through
        #Honestly this is moreso useful to improve the codebase than to exhaust testing/coverage
    #This obviously fails so commenting out
    # @patch('library.library_db_interface.TinyDB')
    # def test_retrieve_patron_insert_duplicate_id_first(self, mock_tinydb):
    #     mock_db_instance = MagicMock()
    #     mock_tinydb.return_value = mock_db_instance

    #     #First I add two patrons with the same ID
    #     mock_db_instance.search.return_value = [
    #         {'fname': 'John', 'lname': 'Doe', 'age': 25, 'memberID': 'P001', 'borrowed_books': []},
    #         {'fname': 'Jane', 'lname': 'Smith', 'age': 30, 'memberID': 'P001', 'borrowed_books': []}  # Duplicate ID
    #     ]
        
    #     lib_db = library_db_interface.Library_DB()
        
    #     #Then I check to see what happens when I ask for the result
    #     result = lib_db.retrieve_patron("P001")

    #     self.assertIsNotNone(result)
    #     self.assertIsInstance(result, Patron)
    #     self.assertEqual(result.get_memberID(), "P001")
    #     self.assertEqual(result.get_fname(), "Jane")
    #     self.assertEqual(result.get_lname(), "Smith")
    #     self.assertEqual(result.get_age(), 30)
    #     mock_db_instance.search.assert_called_once()
    
    @patch('library.library_db_interface.TinyDB')
    def test_get_all_patrons(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance
        patrons = [
            {'fname': 'John', 'lname': 'Doe', 'age': 25, 'memberID': 'P001'},
            {'fname': 'Jane', 'lname': 'Doe', 'age': 23, 'memberID': 'P002'}
        ]
        mock_db_instance.all.return_value = patrons

        lib_db = library_db_interface.Library_DB()
        result = lib_db.get_all_patrons()

        self.assertEqual(result, patrons)
        mock_db_instance.all.assert_called_once()


    @patch('library.library_db_interface.TinyDB')
    def test_close_database(self, mock_tinydb):
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance

        lib_db = library_db_interface.Library_DB()
        lib_db.close_db()

        mock_db_instance.close.assert_called_once()

    def tearDown(self):
        #Clean up test database file made to prevent actual files being made
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    

    

