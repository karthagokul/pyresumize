from  pyresumizer.candidate import Candidate

from unittest import TestCase

class Emailesting(TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_candidate=Candidate()

    def test_email(self):
       _test_candidate=self._test_candidate
       #Since its a private method
       #Invalid Emails
       result=_test_candidate._Candidate__extract_email("@karthagokul")
       self.assertEqual("",result)
       result=_test_candidate._Candidate__extract_email("karthagokul@gmailcom")
       self.assertEqual("",result)
       result=_test_candidate._Candidate__extract_email("")
       self.assertEqual("",result)
       #valid One
       result=_test_candidate._Candidate__extract_email("karthagokul@gmail.com")
       self.assertEqual("karthagokul@gmail.com",result)
       result=_test_candidate._Candidate__extract_email("karthagokul@yahoo.co.ca")
       self.assertEqual("karthagokul@yahoo.co.ca",result)

    def test_name(self):
       _test_candidate=self._test_candidate
       #Since its a private method
       #Invalid Emails
       result=_test_candidate._Candidate__fetch_name("I am Working")
       self.assertEqual("",result)
       result=_test_candidate._Candidate__fetch_name("Eindhoven is a city in Netherlands")
       self.assertEqual("",result)
       result=_test_candidate._Candidate__fetch_name("")
       self.assertEqual("",result)
       #valid One
       result=_test_candidate._Candidate__fetch_name("Gokul Kartha karthagokul@gmail.com")
       self.assertEqual("Gokul Kartha",result)
       #Todo
       #result=_test_candidate._Candidate__fetch_name("Gokul S kartha")
       #self.assertEqual("Gokul S kartha",result)
       
