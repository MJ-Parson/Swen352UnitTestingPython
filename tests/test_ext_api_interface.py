import unittest
from unittest.mock import MagicMock, patch

import requests;
from library.ext_api_interface import Books_API


class TestBooks_API(unittest.TestCase):

    def setUp(self):
        # make mocks
        self.api = Books_API()


    @patch("requests.get")
    def test_make_request_success(self,mock_get):
        #mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"docs":[{"title":"Test Book"}]}
        mock_get.return_value = mock_response

        url = "http://openlibrary.org/search.json?q=test"
        result = self.api.make_request(url)
        self.assertEqual(result, {"docs": [{"title":"Test Book"}]})
        mock_get.assert_called_once_with(url)

    @patch("requests.get")
    def test_make_request_failure_status(self, mock_get):
        #mock a non200 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.make_request("http://badurl")
        self.assertIsNone(result)

    @patch("requests.get")
    def test_make_request_connection_error(self, mock_get):
        #simulate connection error
        # mock_get.side_effect = Exception("ConnectionError")
        # result = self.api.make_request("http://failurl")
        # print("        [>] "+result)
        # self.assertRaises(Exception("ConnectionError"))
        # self.assertIsInstance(result,Exception("ConnectionError"))
        mock_get.side_effect = requests.exceptions.ConnectionError("Mocked Connection Error")
        result = self.api.make_request("http://failurl")

        # Since original function just says None, check with print statement that we're hitting that code:
        # Success! assert none
        self.assertEqual(result, None)

    @patch.object(Books_API,"make_request")
    def test_is_book_available_true(self,mock_make_request):
        mock_make_request.return_value = {"docs": [{"title":"Some Book"}]}
        result = self.api.is_book_available("Some Book")
        self.assertTrue(result)

    @patch.object(Books_API, "make_request")
    def test_is_book_available_false(self, mock_make_request):
        mock_make_request.return_value = {"docs": []}
        result = self.api.is_book_available("Unknown Book")
        self.assertFalse(result)

    @patch.object(Books_API,"make_request")
    def test_books_by_author(self, mock_make_request):
        mock_make_request.return_value = {
            "docs": [
                {"title_suggest":"Book 1"},{"title_suggest":"Book 2"}
            ]
        }
        result = self.api.books_by_author("Some Author")
        self.assertEqual(result, ["Book 1", "Book 2"])

    @patch.object(Books_API,"make_request")
    def test_books_by_author_no_json(self,mock_make_request):
        mock_make_request.return_value = None
        result = self.api.books_by_author("Jsonovitch Bosch")
        self.assertEqual(result,[])

    @patch.object(Books_API,"make_request")
    def test_get_book_info(self, mock_make_request):
        mock_make_request.return_value = {
            "docs": [
                {"title":"Book 1","publisher":["pub"], "publish_year":[2000], "language":["en"]},
                {"title":"Book 2"}
            ]
        }
        result = self.api.get_book_info("Book 1")
        self.assertEqual(result, [
                {"title":"Book 1","publisher":["pub"], "publish_year":[2000], "language":["en"]},
                {"title":"Book 2"}
        ])

    @patch.object(Books_API,"make_request")
    def test_get_book_info_no_response(self,mock_make_request):
        mock_make_request.return_value = None
        result = self.api.get_book_info("Why I Hate Json: A Memoir")
        self.assertEqual(result,[])

    @patch.object(Books_API,"make_request")
    def test_get_ebooks(self,mock_make_request):
        mock_make_request.return_value = {
            "docs": [
                {"title": "Book 1", "ebook_count_i": 2},
                {"title": "Book 2", "ebook_count_i": 0}
            ]
        }
        result = self.api.get_ebooks("Book One")
        self.assertEqual(result, [{"title": "Book 1", "ebook_count": 2}])
    
    @patch.object(Books_API,"make_request")
    def test_get_ebooks_no_json(self,mock_make_request):
        mock_make_request.return_value = None
        result = self.api.get_ebooks("Json: An Ebook")
        self.assertEqual(result,[])

    def tearDown(self):
        # destroy mocks (don't really need?)
        pass

    
        