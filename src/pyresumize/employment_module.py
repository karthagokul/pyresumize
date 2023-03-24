import os
import re
import spacy
from glob import glob
from pyresumize.interfaces import EmployerBaseInterface
from pyresumize.utilities import Utilities


class EmployerStandardEngine(EmployerBaseInterface):
    def __init__(self, nlp, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = nlp

    def process(self, employment_text):
        """does nothing"""
        candidate_employment = []
        nlp_text = self.nlp(employment_text)
        tokens = [token.text for token in nlp_text if not token.is_stop]
        employ_input_folder = os.path.join(self.config_folder, "employers")
        utils = Utilities()
        employers = utils.generate_keywords_from_csv_files(employ_input_folder)
        employers = list(map(lambda x: str(x).lower(), employers))  # Normalising the Strings to Lower
        # print("found %d employers "%len(employers))

        candidate_employment = []

        tokens = [token.text for token in nlp_text if not token.is_stop]

        # Lets look at the companies with single word
        for token in tokens:
            token = token.lower()
            if token in employers:
                # if token not in candidate_employment:
                candidate_employment.append(token)

        # for the Combined names  such as Operating Systems
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()
            if token in employers:
                candidate_employment.append(token)

        candidate_employment = set(candidate_employment)
        return candidate_employment
