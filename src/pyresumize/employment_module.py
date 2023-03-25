import os
import re
import spacy
from glob import glob
from pyresumize.interfaces import EmployerBaseInterface
from pyresumize.utilities import Utilities
import logging


class EmployerStandardEngine(EmployerBaseInterface):
    def __init__(self, nlp, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = spacy.load("en_core_web_sm", exclude=["entity_ruler"])

        # Override the nlp with custom if needed
        # self.nlp = spacy.load(R"./output/model-best")
        self.__generate_employers()

    def __generate_employers(self):
        employ_input_folder = os.path.join(self.config_folder, "employers")
        utils = Utilities()
        employers = utils.generate_keywords_from_csv_files(employ_input_folder)
        employers = list(map(lambda x: str(x).lower(), employers))  # Normalising the Strings to Lower
        print("found %d employers " % len(employers))
        patterns = []
        ruler = self.nlp.add_pipe("entity_ruler")
        for employer in employers:
            entry = {}
            entry["label"] = "EMPLOYER"
            entry["pattern"] = str(employer)
            patterns.append(entry)
        ruler.add_patterns(patterns)
        self.nlp.to_disk("employers")
        self.nlp_entity = spacy.load("employers")
        self.nlp.remove_pipe("entity_ruler")
        self.nlp.add_pipe("entity_ruler", source=self.nlp_entity)

    def process(self, employment_text):
        """Process the Custom Entity EMPLOYER"""

        doc = self.nlp(employment_text.lower())
        candidate_employment = []
        for ent in doc.ents:
            if ent.label_ == "EMPLOYER":
                candidate_employment.append(ent.text.lower())
                # print(ent.text)
                # print(ent.label_)
        return candidate_employment
