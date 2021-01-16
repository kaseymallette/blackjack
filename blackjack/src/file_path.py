# Import necessary libraries
import os


class Path:
    "Finds the path of a file in the folder /data/ given the filename."

    def __init__(self, file):
        "Instatiate an object that contains a filepath."
        self.get_path(file)


    def get_path(self, file):
        "Use the current working directory to find the path of the file."

        # Get current working directory
        os.getcwd()

        # Change directory from /src/ to /data/
        os.chdir('./')
        path = os.getcwd()
        dir = str(path) + '/data/'

        # Find the file path
        self.path = dir + file
