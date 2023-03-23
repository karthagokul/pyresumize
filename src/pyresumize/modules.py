import os
import re
import spacy
from spacy.matcher import Matcher
import re
import pandas as pdas
from nltk.corpus import stopwords
from os import path
from glob import glob
import nltk

# TODO , See if this need to be done in another place, performance improvements.
nltk.download("stopwords")
# TODO End
config_folder = "data"


def set_config_folder(new_location):
    global config_folder
    config_folder = new_location


from pyresumize.interfaces import (
    EducationBaseInterface,
    NameBaseInterface,
    PhoneBaseInterface,
    EmailBaseInterface,
    SkillBaseInterface,
    EmployerBaseInterface,
)

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


class EducationStandardEngine(EducationBaseInterface):
    def __init__(self, nlp) -> None:
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


class PhoneStandardEngine(PhoneBaseInterface):
    def __init__(self, nlp) -> None:
        super().__init__(config_folder)
        self.nlp = nlp

    def process(self, extracted_text):
        results = set(re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", extracted_text))
        phone = ",".join(results)
        return phone


class NameStandardEngine(NameBaseInterface):
    def __init__(self, nlp) -> None:
        super().__init__(config_folder)
        self.matcher = Matcher(nlp.vocab)
        self.nlp = nlp

    def process(self, extracted_text):
        nlp_text = self.nlp(extracted_text)
        # Identify the Names (Nouns)
        pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]

        self.matcher.add("NAME", [pattern])

        matches = self.matcher(nlp_text)

        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        return ""


class EmployerStandardEngine(EmployerBaseInterface):
    def __init__(self, nlp) -> None:
        super().__init__(config_folder)
        self.nlp = nlp
        pass

    def process(self, extracted_text):
        """does nothing"""
        candidate_employment = []
        nlp_text = self.nlp(extracted_text)

        tokens = [token.text for token in nlp_text if not token.is_stop]
        employ_input_folder = os.path.join(self.config_folder, "employers")
        utils = Utilities()
        employers = utils.generate_keywords_from_csv_files(employ_input_folder)
        employers = list(map(lambda x: str(x).lower(), employers))  # Normalising the Strings to Lower

        candidate_employment = []

        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()  # for the Combined works such as Operating Systems
            if token in employers:
                if token not in candidate_employment:
                    candidate_employment.append(token)
        return candidate_employment


class SkillStandardEngine(SkillBaseInterface):
    def __init__(self, nlp) -> None:
        super().__init__(config_folder)
        self.nlp = nlp

    def process(self, extracted_text):
        """ """
        nlp_text = self.nlp(extracted_text)
        skills = []
        tokens = [token.text for token in nlp_text if not token.is_stop]
        # Iterate through the skills csvs and build info

        skills_input_folder = os.path.join(self.config_folder, "skills")
        utils = Utilities()
        skills = utils.generate_keywords_from_csv_files(skills_input_folder)
        skills = list(map(lambda x: str(x).lower(), skills))  # Normalising the Strings to Lower

        skillset = []

        # For words like JAVA
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)

        # for the Combined works such as Operating Systems
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        # Lets mark it lower
        skillset = list(map(lambda x: str(x).lower(), skillset))
        # Remove duplicate skills, if any
        skillset = set(skillset)

        return skillset


class EmailStandardEngine(EmailBaseInterface):
    def __init__(self, nlp) -> None:
        super().__init__(config_folder)
        self.nlp = nlp
        pass

    def process(self, extracted_text):
        result = ""
        # Regex for finding email
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", extracted_text)
        if email:
            try:
                result = email[0].split()[0].strip(";")
                if result is None:
                    result = ""
            except IndexError:
                return result
        return result
