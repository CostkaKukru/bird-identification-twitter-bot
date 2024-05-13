import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fetch_and_download_images import fetch_links_by_search, download_image

@pytest.fixture(scope="module")
def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_fetch_links_by_search(setup_driver):
    driver = setup_driver

    search_query = "bird"
    download_folder = "bird images"
    num_images = 5

    fetch_links_by_search(search_query, download_image)

    # Check if the images are downloaded
    for i in range(1, num_images + 1):
        image_path = f"{download_folder}/{search_query}/{i}.jpg"
        assert os.path.isfile(image_path)

    # Check if the image source links are written to the file
    with open("img_src_links.csv", "r") as file:
        lines = file.readlines()
        assert len(lines) == num_images + 1  # +1 for the header line
        for line in lines[1:]:
            assert search_query in line
            assert "http" in line