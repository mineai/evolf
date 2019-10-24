class FileUtils:

    @staticmethod
    def get_model_extension(file_name):
        """
        This function finds the extension from the path
        and returns it
        :return:
        """
        dot_index = file_name.find(".")
        assert dot_index != -1, "Invalid Model File Path"
        model_extension = file_name[dot_index:]

        return model_extension