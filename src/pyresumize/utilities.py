from os import path
from glob import glob
import pandas as pdas


class Utilities:
    def generate_keywords_from_csv_files(self, foldername, csv_column=0):
        keywords = []
        files = glob(path.join(foldername, "*.csv"))
        for file in files:
            df = pdas.read_csv(file, on_bad_lines="skip", skiprows=1)
            ## Assumes that the first column is full of skills :)
            matrix2 = df[df.columns[csv_column]].to_numpy()
            new_kws = matrix2.tolist()
            keywords = keywords + new_kws
        return keywords
