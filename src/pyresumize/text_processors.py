from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import io
import os.path


class AbstractFileProcessor:
    """The Abstract class provides an interface to extend the processing functonality
    The module supports PDF and DOCX, But in future if there is a new format comes in the functionality can be extended
    """

    def process(self, path):
        pass


class PDFFileProcessor(AbstractFileProcessor):
    """
    Using the PDF Miner Backend, process a Text file
    """

    def process(self, pdf_path):
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
        except Exception:
            return None
        return text


class DocXFileProcessor(AbstractFileProcessor):
    """
    Currently Uses the python-DocX Module to process the DocX Files
    """

    def process(self, filename):
        doc_text = None
        try:
            document = Document(filename)
        except ValueError as ve:
            doc_text = None
        except PackageNotFoundError:
            doc_text = None
        except Exception as e:
            doc_text = None
        else:
            doc_text = "\n\n".join(paragraph.text for paragraph in document.paragraphs)

        return doc_text


class TextProcessingFactory:
    """
    Factory Interface for text parsing
    """

    def __init__(self) -> None:
        self.processors = {}
        self.processors["docx"] = DocXFileProcessor()
        self.processors["pdf"] = PDFFileProcessor()

    def set_processor(self, customprocessor, extension):
        """
        We can define own processing engine and register it with factory via this method
        """
        self.processors[extension] = customprocessor

    def process(self, filename):
        """
        The worker
        """
        result = None
        extension = os.path.splitext(filename)[1][1:]
        if self.processors[extension]:
            result = self.processors[extension].process(filename)
        else:
            result = None
        return result
