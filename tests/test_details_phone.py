import sys

sys.path.append("src")
from pyresumize.resume_processor import ResumeProcessor
from pyresumize.candidate import Candidate

from unittest import TestCase


class Phoneesting(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_candidate = Candidate()

    def test_phone(self):
        """Checks all kind of Phone formats"""
        _test_candidate = self._test_candidate

        # two numbers case
        result = _test_candidate._Candidate__extract_mobile_number(
            "My Phone number is +919562099376 , can you give me a call? I have another number too +919562099377"
        )
        self.assertEqual("+919562099376,+919562099377", result)

        # One number case
        result = _test_candidate._Candidate__extract_mobile_number("+919562099376")
        self.assertEqual("+919562099376", result)

        # Duplicate number case
        result = _test_candidate._Candidate__extract_mobile_number("+919562099376 Again My Number +919562099376")
        self.assertEqual("+919562099376", result)

        # Invalid one
        result = _test_candidate._Candidate__extract_mobile_number("")
        self.assertEqual("", result)

        result = _test_candidate._Candidate__extract_mobile_number(
            "phone number is +31 611484939 and email is kartha@gmail.com"
        )
        self.assertEqual("+31 611484939", result)

        result = _test_candidate._Candidate__extract_mobile_number(
            "+31(0)611484939 is a different formatted phone :) , Do you know?"
        )
        self.assertEqual("+31(0)611484939", result)
