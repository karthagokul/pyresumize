
import spacy
from spacy.matcher import Matcher
import re
import pandas as pdas
import os
import re
import spacy
from nltk.corpus import stopwords
from os import path
from glob import glob

EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]
STOPWORDS = set(stopwords.words('english'))

class Candidate:
    name=""
    phone=""
    email=""
    personal_details={}
    skills=[]
    nlp = spacy.load('en_core_web_sm')
    config_folder="data"
    matcher = Matcher(nlp.vocab)   

    def process(self,resume_data):
        self.personal_details["name"]=self.__fetch_name(resume_data)
        self.personal_details["phone"]=self.__extract_mobile_number(resume_data)
        self.personal_details["email"]=self.__extract_email(resume_data)
        self.skills=self.__extract_skills(resume_data)
        self.education=self.__extract_education(resume_data)
        self.employers=self.__extract_employment(resume_data)
        return True
    
    def __fetch_name(self,resume_data):
        '''
        TODO : Consider Three Word Names such as Thomas Van Limburg
        '''
        nlp_text = self.nlp(resume_data)
        
        # Identify the Names (Nouns)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        
        self.matcher.add('NAME', [pattern])
        
        matches = self.matcher(nlp_text)
        
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        return ""
    
    def __extract_email(self,text):
        '''
        '''
        result=""
        #Regex for finding email
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                result=email[0].split()[0].strip(';')
                if result is None:
                    result=""
            except IndexError:
                return result
        return result
            
    def __extract_mobile_number(self,text):
        '''Need to Tweak this
        '''
        #Need to improve this , I see that some local phones are not captured
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
        
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number

    
    def __generate_keywords_from_csv_files(self,foldername,csv_column=0):
        keywords=[]
        files=glob(path.join(foldername, "*.csv"))
        for file in files:
            df = pdas.read_csv(file,skiprows=1)
            ## Assumes that the first column is full of skills :)
            matrix2 = df[df.columns[csv_column]].to_numpy()
            new_kws = matrix2.tolist()
            keywords=keywords+new_kws
        return keywords

    def __extract_skills(self,resume_text):
        '''
        '''
        nlp_text = self.nlp(resume_text)
        skills=[]
        tokens = [token.text for token in nlp_text if not token.is_stop]
        #Iterate through the skills csvs and build info
        skills_input_folder=os.path.join(self.config_folder,"skills")
        skills=self.__generate_keywords_from_csv_files(skills_input_folder)
        skills=list(map(lambda x: str(x).lower(), skills)) # Normalising the Strings to Lower       
        
        skillset = []

        #For words like JAVA
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)
    
        # for the Combined works such as Operating Systems
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip() 
            if token in skills:
                skillset.append(token)
        #Lets mark it lower
        skillset=list(map(lambda x: str(x).lower(), skillset))
        #Remove duplicate skills, if any
        skillset = set(skillset)

        return skillset
    
    def __extract_education(self,resume_text):
        '''
        '''
        _text = self.nlp(resume_text)
        _text = [sent.text.strip() for sent in _text.sents]

        degrees = {}

        #Lets search for Single words like BE
        for index, text in enumerate(_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    degrees[tex] = text + _text[index + 1]
        #Now Lets search Longer word like Bachelor of Technology
        # for the Combined works such as Operating Systems
        #TODO , Use Noun Chunks
        #Improve this please
        education={}
        education_map = []
        for key in degrees.keys():
            year = re.search(re.compile(r'(((20)(\d{2})))'), degrees[key]) #Assumes that the year is somewhere in 2000s
            if year:
                education_map.append((key, ''.join(year[0])))
            else:
                education_map.append(key)
        education["entry"]=education_map
        education["universities"]=self.__find_universities(resume_text)
        #Later can be added with university
        return education
    
    def __extract_employment(self,resume_text):
        '''
        '''
        candidate_employment=[]
        nlp_text = self.nlp(resume_text)

        tokens = [token.text for token in nlp_text if not token.is_stop]
        employ_input_folder=os.path.join(self.config_folder,"employers")
        employers=self.__generate_keywords_from_csv_files(employ_input_folder)
        employers=list(map(lambda x: str(x).lower(), employers)) # Normalising the Strings to Lower
       
        candidate_employment = []       
        
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip() # for the Combined works such as Operating Systems
            if token in employers:
                if token not in candidate_employment:
                    candidate_employment.append(token)
        return candidate_employment
    
    def __find_universities(self,resume_text):
        '''
        '''
        nlp_text = self.nlp(resume_text)

        tokens = [token.text for token in nlp_text if not token.is_stop]
        universities_input_folder=os.path.join(self.config_folder,"universities")
        universities=self.__generate_keywords_from_csv_files(universities_input_folder)
        universities=list(map(lambda x: str(x).lower(), universities)) # Normalising the Strings to Lower
       
        candidate_universities = []       
        
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip() # for the Combined works such as Operating Systems
            if token in universities:
                candidate_universities.append(token)

        return candidate_universities