import os
import pytest
from dataset_utils import check_dataset_directory, check_image_file

@pytest.fixture(scope="module")
def setup_dataset():
    os.makedirs("dataset/class1")
    os.makedirs("dataset/class2")
    open("dataset/class1/image1.jpg", 'a').close()
    open("dataset/class1/image2.jpg", 'a').close()
    open("dataset/class2/image3.jpg", 'a').close()

    yield

    os.remove("dataset/class1/image1.jpg")
    os.remove("dataset/class1/image2.jpg")
    os.remove("dataset/class2/image3.jpg")
    os.rmdir("dataset/class1")
    os.rmdir("dataset/class2")


def test_check_image_file(setup_dataset):
    valid_image_path = "dataset/class1/image1.jpg"
    assert check_image_file(valid_image_path) is True

    invalid_image_path = "dataset/class1/non_existent_image.jpg"
    assert check_image_file(invalid_image_path) is False

    invalid_image_path = "dataset/class1/invalid_file.txt"
    assert check_image_file(invalid_image_path) is False

