import os
from PIL import Image
import glob

dataset_dirname = "bird images"

def read_images():
    image_list = []

    for filename in glob.glob('.\\bird images\\*\\*.jpg'):
        if "_full.jpg" in filename:
            print(filename)
            os.remove(filename)
        else:
            image_list.append(filename)

    print(len(image_list))

def read_classes():
    """
    Reads the classes (directory names) from the specified dataset directory.

    Returns:
        A list of directory names representing the classes in the dataset directory.
    """
    dirfiles = os.listdir(dataset_dirname)
    fullpaths = map(lambda name: os.path.join(dataset_dirname, name), dirfiles)
    dirs = []

    for file in fullpaths:
        if os.path.isdir(file):
            class_name = file.split("\\")[1]
            dirs.append(class_name)
            
    return dirs

def main():
    return read_classes();

main()