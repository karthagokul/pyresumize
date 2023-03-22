import sys

sys.path.append("src")
from pyresumize.resume_processor import ResumeProcessor
from pyresumize.candidate import Candidate

from unittest import TestCase


class Nameesting(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_candidate = Candidate()

    def test_name(self):
        _test_candidate = self._test_candidate
        # Since its a private method
        result = _test_candidate._Candidate__fetch_name("I am Working")
        self.assertEqual("", result)
        result = _test_candidate._Candidate__fetch_name("Eindhoven is a city in Netherlands")
        self.assertEqual("", result)
        result = _test_candidate._Candidate__fetch_name("")
        self.assertEqual("", result)
        # valid One
        result = _test_candidate._Candidate__fetch_name("Gokul Kartha karthagokul@gmail.com")
        self.assertEqual("Gokul Kartha", result)
        # Todo
        # result=_test_candidate._Candidate__fetch_name("Gokul S kartha")
        # self.assertEqual("Gokul S kartha",result)
