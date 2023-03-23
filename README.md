
  

  

![](https://github.com/karthagokul/pyresumize/blob/main/logo.png?raw=true)

# Introduction
  

pyresumize is a python module to extract useful information from resume and generate a json string out of it. Currently it supports only pdf file as input .


### Todo

* Implement a Skill Fetcher
* Support for other formats
* Performance Improvements 
* Bug Fixes
* Custom configuration of input data

### Note

The Skills , Employers and Education is given as .csv inputs to the engine and you can see a reference implementation in the data folder.


### Design  

I have changed the Design in such a way that the developers can create own parsing rules and set those to the Parser to bring in flexibility. 

Currently we have the below interfaces exposed and the developers can override the process method to bring in custom processing rules.  

- EmployerBaseInterface:

Searches for company information in the resume and identifies the employers

- EducationBaseInterface

Process Education Details together with universities .The results are stored in a map

- EmailBaseInterface

Check for email addresses in the resume and returns if found one.

- PhoneBaseInterface

Process phone numbers in the resume text, if there are more than one phone number found , returns a concatenated string with commas.

- NameBaseInterface

Proces the Name of the candidate .

- SkillBaseInterface:

Process the skills section . returns a list of identified skills in a resume.

One of these interfaces can be implemented like below . 

    class RemoteCompaniesChecker (EmployerBaseInterface):
        def process(self,resumetext):
        #Call a remote API and pass the text info
        return list[]

  
The ResumeEngine class has below member functions and with one of these you can apply your custom engine

    set_skills_engine(self, engine):    
    set_name_engine(self, engine):    
    set_name_engine(self, engine):    
    set_email_engine(self, engine):    
    set_education_engine(self, engine):    
    set_employer_engine(self, engine):

## Usage  

https://pypi.org/project/pyresumize/ . The module can be install using


    pip install pyresumize

 
Then do the below


    python -m spacy download en_core_web_sm    
    python -m nltk.downloader words    
    python -m nltk.downloader stopwords    
    from pyresumize import ResumeEngine    
    r_parser=ResumeEngine()    
    r_parser.set_custom_keywords_folder("data")    
    json=r_parser.process_resume(file)    
    print(json)
