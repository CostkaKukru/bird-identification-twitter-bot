import unittest
from unittest.mock import patch, MagicMock, mock_open
from selenium.webdriver.remote.webelement import WebElement
import requests
import os

# Import the module under test
import fetch_and_download_images

class TestFetchLinksBySearch(unittest.TestCase):
    @patch('fetch_and_download_images.webdriver.Chrome')
    @patch('fetch_and_download_images.WebDriverWait')
    def test_fetch_links_by_search(self, mock_wait, mock_chrome):
        # Mock the Chrome WebDriver instance
        mock_driver = mock_chrome.return_value

        # Mock the WebDriverWait instance
        mock_wait_instance = mock_wait.return_value
        mock_wait_instance.until.return_value = WebElement(mock_driver, 'id')

        # Mock the search box element
        mock_search_box = MagicMock()
        mock_driver.find_element.return_value = mock_search_box

        # Call the function with a test search query
        fetch_and_download_images.fetch_links_by_search('test query', MagicMock())

        # Assert that the WebDriver was initialized with the correct options
        mock_chrome.assert_called_once()

        # Assert that the search box was found and the query was entered
        mock_driver.find_element.assert_called_once_with(fetch_and_download_images.By.NAME, "q")
        mock_search_box.send_keys.assert_called_once_with('test query')
        mock_search_box.submit.assert_called_once()

class TestDownloadImage(unittest.TestCase):
    @patch('os.path.isdir', return_value=False)
    @patch('os.makedirs')
    @patch('requests.get')
    def test_download_image(self, mock_get, mock_makedirs, mock_isdir):
        # Mock the response from requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = b'image content'

        # Mock the open function
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            fetch_and_download_images.download_image('http://example.com/image.jpg', 'folder', 'query', 1)

        # Assert that the directory was created
        mock_isdir.assert_called_once_with('folder/query')
        mock_makedirs.assert_called_once_with('folder/query')

        # Assert that the image was downloaded
        mock_get.assert_called_once_with('http://example.com/image.jpg')

        # Assert that the image was written to a file
        mock_file.assert_called_once_with('folder/query/1.jpg', 'wb')
        handle = mock_file()
        handle.write.assert_called_once_with(b'image content')

if __name__ == '__main__':
    unittest.main()