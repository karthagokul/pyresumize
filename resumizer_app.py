import sys
import os
from os import path
from glob import glob
import json

sys.path.append("src")
from pyresumize.resume_processor import ResumeEngine

# global instance of parser, Since we use Spacy models , this helps to reduce load time
r_parser = ResumeEngine()


def process_resume(file_name):
    global r_parser
    r_parser.set_custom_keywords_folder("data")
    return r_parser.process_resume(file_name)


def find_ext(dr, ext):
    files = []
    files = [
        os.path.join(dp, f) for dp, dn, filenames in os.walk(dr) for f in filenames if os.path.splitext(f)[1] == ext
    ]
    return files


def main():
    """find the files in a given folder with extension pdf and process those"""
    if len(sys.argv) < 2:
        print("Error : The resume folder to be specified as command line argument")
        sys.exit(-1)
    foldername = str(sys.argv[1])
    pdf_files = find_ext(foldername, ".pdf")
    docx_files = find_ext(foldername, ".docx")
    files = pdf_files + docx_files
    counter = 0
    for file in files:
        counter += 1
        print("\n[%d/%d] Filename: %s " % (counter, len(files), file))
        result = process_resume(file)
        print(result)


if __name__ == "__main__":
    main()
