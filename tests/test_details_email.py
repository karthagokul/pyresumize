import sys

sys.path.append("src")
import spacy
from pyresumize.basic_details_module import (
    NameStandardEngine,
    PhoneStandardEngine,
    EmailStandardEngine,
)
from pyresumize.education_module import EducationStandardEngine
from pyresumize.skills_module import SkillStandardEngine
from pyresumize.employment_module import EmployerStandardEngine

from unittest import TestCase


class Emailesting(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_email(self):
        self.nlp = spacy.load("en_core_web_sm")
        engine = EmailStandardEngine(self.nlp, "data")
        # Since its a private method
        # Invalid Emails
        result = engine.process("@karthakul")
        self.assertEqual("", result)
        result = engine.process("karth@gmailcom")
        self.assertEqual("", result)
        result = engine.process("")
        self.assertEqual("", result)
        # valid One
        result = engine.process("gokul@gmail.com")
        self.assertEqual("gokul@gmail.com", result)
        result = engine.process("karthagokul@yahoo.co.ca")
        self.assertEqual("karthagokul@yahoo.co.ca", result)
