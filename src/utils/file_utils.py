import os

class FileUtils:
    @staticmethod
    def make_sure_directory_exists(directory):
        """
        Ensure that the specified directory exists. If it does not exist, create it.

        :param directory: The path to the directory to check/create.
        :type directory: str
        """
        if not os.path.exists(directory):
            os.makedirs(directory)