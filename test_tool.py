from pyresumizer import ResumeProcessor

r_parser=ResumeProcessor()
json=r_parser.process_resume("")
print(json)