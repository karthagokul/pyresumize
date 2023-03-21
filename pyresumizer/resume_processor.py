from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

class ResumeProcessor:
    def __init__(self) -> None:
        '''
        '''
        pass

    def process_resume(self,file_path):
        '''
        '''
        data={}
        #Check if file is a pdf / doc and process accordingly.
        return data

    def __extract_text_from_pdf(self,pdf_path):
        '''
        '''
        text=""
        with open(pdf_path, 'rb') as fh:
            # iterate over all pages of PDF document
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                # creating a resoure manager
                resource_manager = PDFResourceManager()

                # create a file handle
                fake_file_handle = io.StringIO()

                # creating a text converter object
                converter = TextConverter(
                                    resource_manager,
                                    fake_file_handle,
                                    codec='utf-8',
                                    laparams=LAParams()
                            )

                # creating a page interpreter
                page_interpreter = PDFPageInterpreter(
                                    resource_manager,
                                    converter
                                )

                # process current page
                page_interpreter.process_page(page)

                # extract text
                text += fake_file_handle.getvalue()

                # close open handles
                converter.close()
                fake_file_handle.close()
            return text
