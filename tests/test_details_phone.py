import sys
import spacy

sys.path.append("src")

from pyresumize.basic_details_module import (
    NameStandardEngine,
    PhoneStandardEngine,
    EmailStandardEngine,
)
from pyresumize.education_module import EducationStandardEngine
from pyresumize.skills_module import SkillStandardEngine
from pyresumize.employment_module import EmployerStandardEngine

from unittest import TestCase


class Phoneesting(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_phone(self):
        self.nlp = spacy.load("en_core_web_sm")
        engine = PhoneStandardEngine(self.nlp, "data")

        # two numbers case
        result = engine.process(
            "My Phone number is +919562099376 , can you give me a call? I have another number too +919562099377"
        )
        ans_1 = "+919562099376"
        ans_2 = "+919562099377"
        self.assertEqual(ans_1 in result, True)
        self.assertEqual(ans_2 in result, True)

        # One number case
        result = engine.process("+919562099376")
        self.assertEqual("+919562099376", result)

        # Duplicate number case
        result = engine.process("+919562099376 Again My Number +919562099376")
        self.assertEqual("+919562099376", result)

        # Invalid one
        result = engine.process("")
        self.assertEqual("", result)

        result = engine.process("phone number is +31 611484939 and email is kartha@gmail.com")
        self.assertEqual("+31 611484939", result)

        result = engine.process("+31(0)611484939 is a different formatted phone :) , Do you know?")
        self.assertEqual("+31(0)611484939", result)
