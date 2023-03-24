import re
from spacy.matcher import Matcher
from nltk.corpus import stopwords
from os import path
from glob import glob
from pyresumize.interfaces import PhoneBaseInterface, NameBaseInterface, EmailBaseInterface


class PhoneStandardEngine(PhoneBaseInterface):
    """
    Engine which uses a Regular expression to parse the phone number
    TODO: Currently it supports only international formats, Need improvement with better filterations
    """

    def __init__(self, nlp, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = nlp

    def process(self, extracted_text):
        results = set(re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", extracted_text))
        phone = ",".join(results)
        return phone


class NameStandardEngine(NameBaseInterface):
    """
    Engine to get the Name of the candidate
    TODO : Only supports Two worded names , If there are three words , it is not supported
    """

    def __init__(self, nlp, config_folder) -> None:
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


class EmailStandardEngine(EmailBaseInterface):
    """
    Process the email addresses from a Resume
    """

    def __init__(self, nlp, config_folder) -> None:
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
