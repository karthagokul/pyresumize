from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import spacy
from spacy.matcher import Matcher
import os
from pyresumize.utilities import Utilities
import pyresumize.modules as modules
from pyresumize.modules import (
    SkillStandardEngine,
    NameStandardEngine,
    PhoneStandardEngine,
    EmailStandardEngine,
    EducationStandardEngine,
    EmployerStandardEngine,
)


class Candidate:
    """The Person Class who owns the given resume
    The Extracted data is encapsulated in this class
    """

    name = ""
    phone = ""
    email = ""
    personal_details = {}
    skills = []
    education = {}
    employers = []


class ResumeEngine:
    """The GodFather Class with the API interface"""

    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.candidate = Candidate()
        self.name_engine = NameStandardEngine(self.nlp)
        self.skills_engine = SkillStandardEngine(self.nlp)
        self.phone_engine = PhoneStandardEngine(self.nlp)
        self.email_engine = EmailStandardEngine(self.nlp)
        self.education_engine = EducationStandardEngine(self.nlp)
        self.employer_engine = EmployerStandardEngine(self.nlp)

    def set_skills_engine(self, engine):
        self.skills_engine = engine

    def set_name_engine(self, engine):
        self.name_engine = engine

    def set_name_engine(self, engine):
        self.phone_engine = engine

    def set_email_engine(self, engine):
        self.email_engine = engine

    def set_education_engine(self, engine):
        self.education_engine = engine

    def set_employer_engine(self, engine):
        self.employer_engine = engine

    def set_custom_keywords_folder(self, folder_name):
        modules.set_config_folder(folder_name)

    def __generate_json(self):
        """
        Generates the respective json format of the resume
        """
        json_data = {}
        json_data["basic_details"] = self.candidate.personal_details
        json_data["skills"] = self.candidate.skills
        json_data["education"] = self.candidate.education
        json_data["employers"] = self.candidate.employers
        return json_data

    def check_file_sanity(self, file_path):
        """
        Utility function to check if the file given is valid
        """
        return self.__extract_text_from_pdf(file_path)

    def process_resume(self, file_path):
        """
        The Worker API !
        """
        resume_data = self.__extract_text_from_pdf(file_path)
        if resume_data is None:
            util = Utilities()
            return util.error_handler("File %s Can not be opened" % (file_path))
        self.candidate.name = self.name_engine.process(resume_data)
        self.candidate.skills = self.skills_engine.process(resume_data)
        self.candidate.personal_details["phone"] = self.phone_engine.process(resume_data)
        self.candidate.personal_details["email"] = self.email_engine.process(resume_data)
        self.candidate.education = self.education_engine.process(resume_data)

        data = self.__generate_json()
        # Check if file is a pdf / doc and process accordingly.
        return data

    def __extract_text_from_pdf(self, pdf_path):
        """Get All text from PDF"""
        text = ""
        try:
            with open(pdf_path, "rb") as fh:
                # iterate over all pages of PDF document
                for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager, fake_file_handle, codec="utf-8", laparams=LAParams())
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)
                    text += fake_file_handle.getvalue()
                    fake_file_handle.close()
        except:
            # print("Unable to Process file %s"%pdf_path)
            # Any parsing failure we handle here .
            return None

        return text
