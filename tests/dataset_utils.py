import os
import glob
from PIL import Image

def check_dataset_directory(dataset_dirname):
    return os.path.exists(dataset_dirname)

def check_image_file(file):
    try:
        img = Image.open(file)
        img.verify()  # Verify if it's a valid image file
        return True
    except (IOError, SyntaxError):
        return False

def read_images(dataset_dirname):
    if not check_dataset_directory(dataset_dirname):
        return None
    
    image_list = []
    for filename in glob.glob(os.path.join(dataset_dirname, '*', '*.jpg')):
        if "_full.jpg" in filename:
            print("Removing redundant file:", filename)
            os.remove(filename)
        else:
            image_list.append(filename)

    print("Total valid images:", len(image_list))
    return image_list

def read_classes(dataset_dirname):
    if not check_dataset_directory(dataset_dirname):
        return None
    
    dirs = []
    for dirpath, dirnames, filenames in os.walk(dataset_dirname):
        for dirname in dirnames:
            dirs.append(dirname)
    return dirs
