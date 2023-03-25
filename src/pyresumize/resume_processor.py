import spacy
import nltk
import logging
import json

from pyresumize.utilities import Utilities
from pyresumize.basic_details_module import (
    NameStandardEngine,
    PhoneStandardEngine,
    EmailStandardEngine,
)
from pyresumize.education_module import EducationStandardEngine
from pyresumize.skills_module import SkillStandardEngine
from pyresumize.employment_module import EmployerStandardEngine
from pyresumize.text_processors import TextProcessingFactory

config_folder = "data"

logging.basicConfig(
    level=logging.WARNING, filename="pyresumize.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

# TODO , See if this need to be done in another place, performance improvements.
nltk.download("stopwords")
# TODO End


class Candidate:
    """The Person Class who owns the given resume
    The Extracted data is encapsulated in this class
    """

    personal_details = {}
    skills = []
    education = {}
    employers = []


class ResumeEngine:
    """The GodFather Class with the API interface"""

    def __init__(self) -> None:
        # move this outside , loading a set takes time
        self.nlp = spacy.load("en_core_web_lg")  # Must have for names
        self.candidate = Candidate()
        self.name_engine = NameStandardEngine(self.nlp, config_folder)
        self.skills_engine = SkillStandardEngine(self.nlp, config_folder)
        self.phone_engine = PhoneStandardEngine(self.nlp, config_folder)
        self.email_engine = EmailStandardEngine(self.nlp, config_folder)
        self.education_engine = EducationStandardEngine(self.nlp, config_folder)
        self.employer_engine = EmployerStandardEngine(self.nlp, config_folder)
        self.text_factory = TextProcessingFactory()

    def set_skills_engine(self, engine):
        self.skills_engine = engine

    def set_name_engine(self, engine):
        self.name_engine = engine

    def set_phone_engine(self, engine):
        self.phone_engine = engine

    def set_email_engine(self, engine):
        self.email_engine = engine

    def set_education_engine(self, engine):
        self.education_engine = engine

    def set_employer_engine(self, engine):
        self.employer_engine = engine

    def set_custom_keywords_folder(self, folder_name):
        global config_folder
        config_folder = folder_name

    def add_custom_text_processor(self, processor, file_extension):
        self.text_factory.set_processor(processor, file_extension)

    def __generate_json(self, file_path):
        """
        Generates the respective json format of the resume
        """
        json_data = {}
        json_data["file_name"] = file_path
        json_data["basic_details"] = self.candidate.personal_details
        json_data["skills"] = ",".join(self.candidate.skills)
        json_data["education"] = self.candidate.education
        json_data["employers"] = ",".join(self.candidate.employers)
        return json.dumps(json_data)

    def process_resume(self, file_path):
        """
        The Worker API !
        """
        resume_data = self.text_factory.process(file_path)
        if resume_data == None:
            util = Utilities()
            return util.error_handler("File %s is not supported" % (file_path))

        self.candidate.skills = self.skills_engine.process(resume_data)
        self.candidate.personal_details["name"] = self.name_engine.process(resume_data)
        self.candidate.personal_details["phone"] = self.phone_engine.process(resume_data)
        self.candidate.personal_details["email"] = self.email_engine.process(resume_data)
        self.candidate.education = self.education_engine.process(resume_data)
        self.candidate.employers = self.employer_engine.process(resume_data)

        return self.__generate_json(file_path)
