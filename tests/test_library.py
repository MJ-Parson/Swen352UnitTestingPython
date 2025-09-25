import unittest
from unittest.mock import Mock, patch

from library.library import Library
from library.patron import Patron
import library.library


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

    def test_is_ebook_returns_true_when_book_found(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 1}
        ]
        result = self.library.is_ebook("Test Book")
        self.assertTrue(result)

    def test_is_ebook_returns_true_case_insensitive(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 1}
        ]
        result = self.library.is_ebook("test book")
        self.assertTrue(result)

    def test_is_ebook_returns_false_when_book_not_found(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Different Book', 'ebook_count': 1}
        ]
        result = self.library.is_ebook("Test Book")
        self.assertFalse(result)

    def test_is_ebook_returns_false_when_no_ebooks(self):
        self.mock_api.get_ebooks.return_value = []
        result = self.library.is_ebook("Test Book")
        self.assertFalse(result)

    def test_get_ebooks_count_single_book(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 3}
        ]
        result = self.library.get_ebooks_count("Test Book")
        self.assertEqual(result, 3)

    def test_get_ebooks_count_multiple_books(self):
        self.mock_api.get_ebooks.return_value = [
            {'title': 'Test Book', 'ebook_count': 3},
            {'title': 'Test Book Vol 2', 'ebook_count': 2}
        ]
        result = self.library.get_ebooks_count("Test Book")
        self.assertEqual(result, 5)

    def test_get_ebooks_count_no_books(self):
        self.mock_api.get_ebooks.return_value = []
        result = self.library.get_ebooks_count("Test Book")
        self.assertEqual(result, 0)

    def test_is_book_by_author_returns_true(self):
        self.mock_api.books_by_author.return_value = [
            "Test Book", "Another Book"
        ]
        result = self.library.is_book_by_author("Test Author", "Test Book")
        self.assertTrue(result)

    def test_is_book_by_author_returns_true_case_insensitive(self):
        self.mock_api.books_by_author.return_value = [
            "Test Book", "Another Book"
        ]
        result = self.library.is_book_by_author("Test Author", "test book")
        self.assertTrue(result)

    def test_is_book_by_author_returns_false(self):
        self.mock_api.books_by_author.return_value = [
            "Different Book", "Another Book"
        ]
        result = self.library.is_book_by_author("Test Author", "Test Book")
        self.assertFalse(result)

    def test_is_book_by_author_no_books(self):
        self.mock_api.books_by_author.return_value = []
        result = self.library.is_book_by_author("Test Author", "Test Book")
        self.assertFalse(result)

    def test_get_languages_for_book_single_language(self):
        self.mock_api.get_book_info.return_value = [
            {'title': 'Test Book', 'language': ['eng']}
        ]
        result = self.library.get_languages_for_book("Test Book")
        self.assertEqual(result, {'eng'})

    def test_get_languages_for_book_multiple_languages(self):
        self.mock_api.get_book_info.return_value = [
            {'title': 'Test Book', 'language': ['eng', 'spa']},
            {'title': 'Test Book Ed 2', 'language': ['fra']}
        ]
        result = self.library.get_languages_for_book("Test Book")
        self.assertEqual(result, {'eng', 'spa', 'fra'})

    def test_get_languages_for_book_no_language_key(self):
        self.mock_api.get_book_info.return_value = [
            {'title': 'Test Book'}
        ]
        result = self.library.get_languages_for_book("Test Book")
        self.assertEqual(result, set())

    def test_get_languages_for_book_no_books(self):
        self.mock_api.get_book_info.return_value = []
        result = self.library.get_languages_for_book("Test Book")
        self.assertEqual(result, set())

    @patch('library.library.Patron')
    def test_register_patron_success(self, mock_patron_class):
        mock_patron_instance = Mock()
        mock_patron_class.return_value = mock_patron_instance
        self.mock_db.insert_patron.return_value = 1

        result = self.library.register_patron("Uttam", "Bhattarai", 23, "12345")

        mock_patron_class.assert_called_with("Uttam", "Bhattarai", 23, "12345")
        self.mock_db.insert_patron.assert_called_with(mock_patron_instance)
        self.assertEqual(result, 1)



if __name__ == '__main__':
    unittest.main()