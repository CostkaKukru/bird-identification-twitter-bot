import os
import pytest
from dataset_utils import check_dataset_directory, check_image_file

@pytest.fixture(scope="module")
def setup_dataset():
    # Create a temporary dataset directory structure for testing
    os.makedirs("dataset/class1")
    os.makedirs("dataset/class2")
    open("dataset/class1/image1.jpg", 'a').close()
    open("dataset/class1/image2.jpg", 'a').close()
    open("dataset/class2/image3.jpg", 'a').close()

    yield

    # Remove the temporary dataset directory after testing
    os.remove("dataset/class1/image1.jpg")
    os.remove("dataset/class1/image2.jpg")
    os.remove("dataset/class2/image3.jpg")
    os.rmdir("dataset/class1")
    os.rmdir("dataset/class2")