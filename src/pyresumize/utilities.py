from os import path
from glob import glob
import pandas as pdas


class Utilities:
    """
    Like in any other module , we also have a utility
    """

    def generate_keywords_from_csv_files(self, foldername, csv_column=0):
        """Given CSV will be loaded and returned as a python list"""
        keywords = []
        files = glob(path.join(foldername, "*.csv"))
        for file in files:
            df = pdas.read_csv(file, on_bad_lines="skip", skiprows=1)
            ## Assumes that the first column is full of skills :)
            matrix2 = df[df.columns[csv_column]].to_numpy()
            new_kws = matrix2.tolist()
            keywords = keywords + new_kws
        return keywords

    def error_handler(self, error_string):
        """The guy who handles errors and inform the user"""
        data = {}
        # The Below Error Code Can be handled globally later :)
        data["error_code"] = -1
        data["error_string"] = error_string
        return data
