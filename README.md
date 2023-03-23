
![](https://github.com/karthagokul/pyresumize/blob/main/logo.png)

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
* EmployerBaseInterface:
* EducationBaseInterface:
* EmailBaseInterface
* PhoneBaseInterface:
* NameBaseInterface:
* SkillBaseInterface:

For More details, please look at the Parser API :)

## Usage
    python -m spacy download en_core_web_sm
    python -m nltk.downloader words
    python -m nltk.downloader stopwords
    from  pyresumize  import ResumeProcessor
    r_parser=ResumeProcessor()
    r_parser.set_custom_keywords_folder("data")
    json=r_parser.process_resume(file)
    print(json)

