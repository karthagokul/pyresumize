from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
from pyresumizer.basic_details import BasicDetails

class ResumeProcessor:
    basic_details=BasicDetails()
    def __init__(self) -> None:
        """ """
        pass

    def process_resume(self, file_path):
        """ """
        text=self.__extract_text_from_pdf(file_path)
        self.basic_details.process(text)
        print("Basic Details")
        print(self.basic_details.personal_details["name"])
        print(self.basic_details.personal_details["phone"])
        print(self.basic_details.personal_details["email"])
        print("Skills")
        print(self.basic_details.skills)
        print("Education")
        print(self.basic_details.education)
        data = {}
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
