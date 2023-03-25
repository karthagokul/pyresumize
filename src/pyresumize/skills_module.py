import os
import spacy
from pyresumize.interfaces import SkillBaseInterface
from pyresumize.utilities import Utilities


class SkillStandardEngine(SkillBaseInterface):
    """The Engine which uses Panda Dataframe to load the Data from CSV directly
    Ideal for processing one or few resumes.
    """

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


class SkillCustomNEREngine(SkillBaseInterface):
    """This Engine Generates a CUSTM NER DB during startup .
    If there are many resumes to be processed in queue . This Engine is much better
    """

    def __init__(self, config_folder) -> None:
        super().__init__(config_folder)
        self.nlp = spacy.load("en_core_web_sm", exclude=["entity_ruler"])
        self.__generate_skills()

    def __generate_skills(self):
        skills_input_folder = os.path.join(self.config_folder, "skills")
        utils = Utilities()
        skills = utils.generate_keywords_from_csv_files(skills_input_folder)
        skills = list(map(lambda x: str(x).lower(), skills))  # Normalising the Strings to Lower
        print("Generating Skills Database: Found %d " % len(skills))
        patterns = []
        ruler = self.nlp.add_pipe("entity_ruler")
        for skill in skills:
            entry = {}
            entry["label"] = "SKILL"
            entry["pattern"] = str(skill)
            patterns.append(entry)
        ruler.add_patterns(patterns)
        self.nlp.to_disk("skills")
        self.nlp_entity = spacy.load("skills")
        self.nlp.remove_pipe("entity_ruler")
        self.nlp.add_pipe("entity_ruler", source=self.nlp_entity)

    def process(self, extracted_text):
        """ """
        doc = self.nlp(extracted_text.lower())
        skills = []
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                skills.append(ent.text.lower())
        # Removes Duplicate
        skills = set(skills)
        return skills
