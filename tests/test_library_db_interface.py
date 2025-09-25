import unittest
from unittest.mock import MagicMock, Mock, patch

import requests
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
    
    # def test_insert_not_patron():
    #     return
    
    # def test_insert_copy_patron():
    #     return
    
    # def test_get_patron_count():
    #     return
    
    # def test_get_patron_count_before_and_after_update():
    #     return
    
    # def test_retrieve_patron_success():
    #     return
    
    # def test_retrieve_patron_invalid():
    #     return
    
    # def test_retrieve_patron_insert_duplicate_id():
    #     #First I add two patrons with the same ID

    #     #Then I check to see what happens when I ask for the result
    #     return
    
    # def test_close_database():
    #     return
    
    def tearDown(self):
        #Clean up test database file made to prevent actual files being made
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    

    

