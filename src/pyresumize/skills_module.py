import os
import re
import spacy
from glob import glob
from pyresumize.interfaces import SkillBaseInterface
from pyresumize.utilities import Utilities


class SkillStandardEngine(SkillBaseInterface):
    def __init__(self, nlp, config_folder) -> None:
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
