import unittest
import os
import dataset_utils

class TestScript(unittest.TestCase):
    def setUp(self):
        # Create a temporary dataset directory structure for testing
        os.makedirs("dataset/class1")
        os.makedirs("dataset/class2")
        open("dataset/class1/image1.jpg", 'a').close()
        open("dataset/class1/image2.jpg", 'a').close()
        open("dataset/class2/image3.jpg", 'a').close()
    
    def tearDown(self):
        # Remove the temporary dataset directory after testing
        os.remove("dataset/class1/image1.jpg")
        os.remove("dataset/class1/image2.jpg")
        os.remove("dataset/class2/image3.jpg")
        os.rmdir("dataset/class1")
        os.rmdir("dataset/class2")
    
    def test_check_image_file(self):
        # Test valid image file
        valid_image_path = "dataset/class1/image1.jpg"
        self.assertTrue(dataset_utils.check_image_file(valid_image_path))
        
        # Test invalid image file (non-existent file)
        invalid_image_path = "dataset/class1/non_existent_image.jpg"
        self.assertFalse(dataset_utils.check_image_file(invalid_image_path))
        
        # Test invalid image file (non-image file)
        invalid_image_path = "dataset/class1/invalid_file.txt"
        self.assertFalse(dataset_utils.check_image_file(invalid_image_path))
    
    def test_check_dataset_directory(self):
        # Test valid dataset directory
        self.assertTrue(dataset_utils.check_dataset_directory("dataset"))
        
        # Test invalid dataset directory (non-existent directory)
        self.assertFalse(dataset_utils.check_dataset_directory("non_existent_dataset"))
        
        # Test invalid dataset directory (not a directory)
        open("invalid_dataset", 'a').close()  # Create a file with the same name
        self.assertFalse(dataset_utils.check_dataset_directory("invalid_dataset"))
        os.remove("invalid_dataset")  # Remove the file for tearDown
    
if __name__ == "__main__":
    unittest.main()
