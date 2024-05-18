import pytest
from unittest.mock import patch, MagicMock, mock_open
from selenium.webdriver.remote.webelement import WebElement
import requests
import os
import fetch_and_download_images

# Import the module under test

@pytest.fixture
def mock_chrome_driver():
    with patch('fetch_and_download_images.webdriver.Chrome') as mock_chrome:
        yield mock_chrome.return_value

@pytest.fixture
def mock_wait():
    with patch('fetch_and_download_images.WebDriverWait') as mock_wait:
        yield mock_wait.return_value

@pytest.fixture
def mock_search_box(mock_chrome_driver):
    mock_search_box = MagicMock()
    mock_chrome_driver.find_element.return_value = mock_search_box
    return mock_search_box

@pytest.fixture
def mock_response():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = b'image content'
        yield mock_response

@pytest.fixture
def mock_file(mock_response):
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

def test_fetch_links_by_search(mock_chrome_driver, mock_wait, mock_search_box):
    # Mock the WebDriverWait instance
    mock_wait_instance = mock_wait.return_value
    mock_wait_instance.until.return_value = WebElement(mock_chrome_driver, 'id')

    # Call the function with a test search query
    fetch_and_download_images.fetch_links_by_search('test query', MagicMock())

    # Assert that the WebDriver was initialized with the correct options
    mock_chrome_driver.assert_called_once()

    # Assert that the search box was found and the query was entered
    mock_chrome_driver.find_element.assert_called_once_with(fetch_and_download_images.By.NAME, "q")
    mock_search_box.send_keys.assert_called_once_with('test query')
    mock_search_box.submit.assert_called_once()

def test_download_image(mock_file):
    # Mock the isdir function
    with patch('os.path.isdir', return_value=False) as mock_isdir:
        fetch_and_download_images.download_image('http://example.com/image.jpg', 'folder', 'query', 1)

        # Assert that the directory was created
        mock_isdir.assert_called_once_with('folder/query')
        os.makedirs.assert_called_once_with('folder/query')

        # Assert that the image was downloaded
        requests.get.assert_called_once_with('http://example.com/image.jpg')

        # Assert that the image was written to a file
        mock_file.assert_called_once_with('folder/query/1.jpg', 'wb')
        handle = mock_file()
        handle.write.assert_called_once_with(b'image content')
