import unittest
from unittest.mock import Mock, patch

from library.library import Library
from library.patron import Patron


class TestLibrary(unittest.TestCase):

    @patch('library.library_db_interface.TinyDB')
    def setUp(self, mock_tinydb):
        mock_db_instance = Mock()
        mock_tinydb.return_value = mock_db_instance

        self.library = Library()

        self.mock_db = Mock()
        self.mock_api = Mock()

        self.library.db = self.mock_db
        self.library.api = self.mock_api

        self.test_patron = Patron("Uttam", "Bhattarai", 23, "12345")

    def test_is_ebook_found(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 1}
        ]
        result = self.library.is_ebook("test book")
        self.assertTrue(result)

    def test_is_ebook_not_found(self):
        self.mock_api.get_ebooks.return_value = []
        result = self.library.is_ebook("Test Book")
        self.assertFalse(result)

    def test_get_ebooks_count(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 3},
            {'title': 'Test Book Vol 2', 'ebook_count': 2}
        ]
        result = self.library.get_ebooks_count("Test Book")
        self.assertEqual(result, 5)

    def test_is_book_by_author_found(self):
        self.mock_api.books_by_author.return_value = ["Test Book"]
        result = self.library.is_book_by_author("Test Author", "test book")
        self.assertTrue(result)

    def test_is_book_by_author_not_found(self):
        self.mock_api.books_by_author.return_value = []
        result = self.library.is_book_by_author("Test Author", "Test Book")
        self.assertFalse(result)

    def test_get_languages_for_book(self):
        self.mock_api.get_book_info.return_value = [
            {'title': 'Test Book', 'language': ['eng', 'spa']},
            {'title': 'Test Book Ed 2'}
        ]
        result = self.library.get_languages_for_book("Test Book")
        self.assertEqual(result, {'eng', 'spa'})

    @patch('library.library.Patron')
    def test_register_patron(self, mock_patron_class):
        mock_patron_instance = Mock()
        mock_patron_class.return_value = mock_patron_instance
        self.mock_db.insert_patron.return_value = 1

        result = self.library.register_patron("Uttam", "Bhattarai", 23, "12345")
        self.assertEqual(result, 1)

    def test_is_patron_registered_true(self):
        self.mock_db.retrieve_patron.return_value = self.test_patron
        result = self.library.is_patron_registered(self.test_patron)
        self.assertTrue(result)

    def test_is_patron_registered_false(self):
        self.mock_db.retrieve_patron.return_value = None
        result = self.library.is_patron_registered(self.test_patron)
        self.assertFalse(result)

    def test_borrow_book(self):
        mock_patron = Mock()
        self.library.borrow_book("Test Book", mock_patron)
        mock_patron.add_borrowed_book.assert_called_with("test book")

    def test_return_borrowed_book(self):
        mock_patron = Mock()
        self.library.return_borrowed_book("Test Book", mock_patron)
        mock_patron.return_borrowed_book.assert_called_with("test book")

    def test_is_book_borrowed_true(self):
        mock_patron = Mock()
        mock_patron.get_borrowed_books.return_value = ["test book"]
        result = self.library.is_book_borrowed("Test Book", mock_patron)
        self.assertTrue(result)

    def test_is_book_borrowed_false(self):
        mock_patron = Mock()
        mock_patron.get_borrowed_books.return_value = []
        result = self.library.is_book_borrowed("Test Book", mock_patron)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()