import sys
import os

sys.path.append("src")
from pyresumize.resume_processor import ResumeEngine
from os import path
from glob import glob

# import time
# Lets download programtically if needed when deploy as service
# import spacy.cli
# spacy.cli.download("en_core_web_lg")


def find_ext(dr, ext):
    files = []
    files = [
        os.path.join(dp, f) for dp, dn, filenames in os.walk(dr) for f in filenames if os.path.splitext(f)[1] == ext
    ]
    return files


r_parser = ResumeEngine()
r_parser.set_custom_keywords_folder("data")
# Lets find the files from a folder of .pdf extension
# t0 = time.time()
files = find_ext(".resumes/working", ".pdf")
for file in files:
    print("Parsing " + file)
    json = r_parser.process_resume(file)
    print(json)
    print("")
# t1 = time.time()
# total = t1-t0
# Print total against the number of resumes to see the performance
