from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
from pyresumize.candidate import Candidate

#TODO , See if this need to be done in another place, performance improvements.
import nltk
nltk.download('stopwords')
#TODO End

class ResumeProcessor:
    candidate=Candidate()
    def __init__(self) -> None:
        """ """
        pass

    def __generate_json(self):
        json_data={}
        json_data["basic_details"]=self.candidate.personal_details
        json_data["skills"]=self.candidate.skills
        json_data["education"]=self.candidate.education
        json_data["employers"]=self.candidate.employers
        return json_data


    def process_resume(self, file_path):
        """ """
        text=self.__extract_text_from_pdf(file_path)
        self.candidate.process(text)
        data = self.__generate_json()
        # Check if file is a pdf / doc and process accordingly.
        return data

   
    def __extract_text_from_pdf(self, pdf_path):
        """Get All text from PDF """
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
        except IOError:
                print('File Open Error')
         
        return text
