from pyresumizer import ResumeProcessor
import nltk
nltk.download('stopwords')

r_parser=ResumeProcessor()
json=r_parser.process_resume("test_file/resume.pdf")
print(json)