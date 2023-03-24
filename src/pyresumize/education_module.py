import os
import re
import spacy
from spacy.matcher import Matcher
import pandas as pdas
from nltk.corpus import stopwords
from os import path
from glob import glob
from pyresumize.interfaces import EducationBaseInterface
from pyresumize.utilities import Utilities


EDUCATION = [
    "BE",
    "B.E.",
    "B.E",
    "BS",
    "B.S",
    "ME",
    "M.E",
    "M.E.",
    "MS",
    "M.S",
    "BTECH",
    "B.TECH",
    "M.TECH",
    "MTECH",
    "SSC",
    "HSC",
    "CBSE",
    "ICSE",
    "X",
    "XII",
]
STOPWORDS = set(stopwords.words("english"))

"""
Below Modules are standard implementations of the respective interfaces
The developer of the library can extend the functionality as in needed by pluggin in a custom module
"""


class EducationStandardEngine(EducationBaseInterface):
    def __init__(self, nlp, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = nlp
        pass

    def process(self, extracted_text):
        _text = self.nlp(extracted_text)
        _text = [sent.text.strip() for sent in _text.sents]

        degrees = {}

        # Lets search for Single words like BE
        for index, text in enumerate(_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r"[?|$|.|!|,]", r"", tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    if len(_text) > index + 1:
                        degrees[tex] = text + _text[index + 1]
        # Now Lets search Longer word like Bachelor of Technology
        # for the Combined works such as Operating Systems
        # TODO , Use Noun Chunks
        # Improve this please
        education = {}
        education_map = []
        for key in degrees.keys():
            year = re.search(
                re.compile(r"(((20)(\d{2})))"), degrees[key]
            )  # Assumes that the year is somewhere in 2000s
            if year:
                education_map.append((key, "".join(year[0])))
            else:
                education_map.append(key)
        education["entry"] = education_map
        education["universities"] = self.__find_universities(extracted_text)
        # Later can be added with university
        return education

    def __find_universities(self, resume_text):
        """ """
        nlp_text = self.nlp(resume_text)

        tokens = [token.text for token in nlp_text if not token.is_stop]
        universities_input_folder = os.path.join(self.config_folder, "universities")
        utils = Utilities()
        universities = utils.generate_keywords_from_csv_files(universities_input_folder)
        universities = list(map(lambda x: str(x).lower(), universities))  # Normalising the Strings to Lower

        candidate_universities = []

        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()  # for the Combined works such as Operating Systems
            if token in universities:
                candidate_universities.append(token)

        return candidate_universities
