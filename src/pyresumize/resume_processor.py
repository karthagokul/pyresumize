from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import docx
import io
import spacy
from pyresumize.utilities import Utilities
import pyresumize.education_module as education_module
from pyresumize.basic_details_module import (
    NameStandardEngine,
    PhoneStandardEngine,
    EmailStandardEngine,
)
from pyresumize.education_module import EducationStandardEngine
from pyresumize.skills_module import SkillStandardEngine
from pyresumize.employment_module import EmployerStandardEngine

config_folder = "data"
import nltk
import logging

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
        # move this outside , loading a set takes time
        self.nlp = spacy.load("en_core_web_lg")
        self.candidate = Candidate()
        self.name_engine = NameStandardEngine(self.nlp, config_folder)
        self.skills_engine = SkillStandardEngine(self.nlp, config_folder)
        self.phone_engine = PhoneStandardEngine(self.nlp, config_folder)
        self.email_engine = EmailStandardEngine(self.nlp, config_folder)
        self.education_engine = EducationStandardEngine(self.nlp, config_folder)
        self.employer_engine = EmployerStandardEngine(self.nlp, config_folder)

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

    def process_resume(self, file_path):
        """
        The Worker API !
        """
        resume_data = None
        if file_path.endswith(".pdf"):
            resume_data = self.__extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            resume_data = self.__extract_text_from_docx(file_path)
        else:
            return util.error_handler("File %s is not supported" % (file_path))
        if resume_data is None:
            util = Utilities()
            return util.error_handler("File %s Can not be opened" % (file_path))
        self.candidate.name = self.name_engine.process(resume_data)
        self.candidate.skills = self.skills_engine.process(resume_data)
        self.candidate.personal_details["phone"] = self.phone_engine.process(resume_data)
        self.candidate.personal_details["email"] = self.email_engine.process(resume_data)
        self.candidate.education = self.education_engine.process(resume_data)
        self.candidate.employers = self.employer_engine.process(resume_data)

        data = self.__generate_json()
        # Check if file is a pdf / doc and process accordingly.
        return data

    def __extract_text_from_docx(self, docx_path):
        document = docx.Document(docx_path)
        doc_text = "\n\n".join(paragraph.text for paragraph in document.paragraphs)
        return doc_text

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
            # Any parsing failure we handle here .
            logging.critical("The File [%s] can not be processed" % pdf_path)
            # Call the Utils.Error handler here ,later stage
            return None

        return text
