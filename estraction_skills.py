import spacy
import re
import pandas as pd
import os
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import HTMLConverter
import io
import  fasttext
import numpy as np
from bs4 import BeautifulSoup
import warnings
from dateparser.search import search_dates
warnings.filterwarnings("ignore")
from utils.cross_functions import CrossFunctions
from utils.job_posts_processing import JobPostsProcessing
from spacy.lang.it.stop_words import STOP_WORDS as it_stop
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.feature_extraction.text import CountVectorizer
np.random.seed(0) 

class FeatureExtraction:
    final_stopwords_list = list(it_stop)

    @staticmethod
    def TFIDF(scraped_data, cv):
        tfidf_vectorizer = TfidfVectorizer(stop_words=FeatureExtraction.final_stopwords_list)

        tfidf_jobid = tfidf_vectorizer.fit_transform(scraped_data)

        user_tfidf = tfidf_vectorizer.transform(cv)

        cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x), tfidf_jobid)

        output = list(cos_similarity_tfidf)
        return [ i[0][0] for  i in  output]

    @staticmethod
    def BOW(scraped_data, cv):
        count_vectorizer = CountVectorizer()

        count_jobid = count_vectorizer.fit_transform(scraped_data)

        user_count = count_vectorizer.transform(cv)
        cos_similarity_countv = map(lambda x: cosine_similarity(user_count, x), count_jobid)
        output = list(cos_similarity_countv)
        return output
class skills_extraction():
   def __init__(self, pdfnamepath,pathmodel,folder):  
       self.pdfnamepath=pdfnamepath
       self.pathmodel=pathmodel
       self.folder=folder
      
       from spacy.lang.it.stop_words import STOP_WORDS
       self.stop = list(spacy.lang.it.stop_words.STOP_WORDS)
       self.stop.extend(['e','i'])
       skills = pd.read_csv(os.path.join(os.getcwd(), "dataset","skills.csv"), encoding='utf-8')
       prog=list(skills.columns)
       filename = os.path.join(os.getcwd(), "dataset",'programming-languages-corrected.csv')
       dffull = pd.read_csv(filename,sep=';', encoding = "ISO-8859-1")
       with open( os.path.join(os.getcwd(), "dataset",'skills_cv.txt')) as f:
            skills_cv = f.read().splitlines() 
       self.namesprogramming=list(set(dffull['ï»¿name'].tolist()+prog+skills_cv)) 
       for i in ['y)','C','D','T','L','E','F','B','S']:
           self.namesprogramming.remove(i)
           
    
       full_occupations = pd.read_csv(os.path.join(os.getcwd(), "dataset","occupation_full.csv"), encoding='utf-8')
   
       self.listjob=pd.read_csv(os.path.join(os.getcwd(), "dataset","jobs_title.csv"), encoding='utf-8',delimiter=';')['jobs'].tolist()
       self.listjob.sort() 
       
       
       full_occupations_skills = full_occupations[['essential_skills', 'optional_skills','isco_group']]
       full_occupations_skills['essential_skills'] = full_occupations_skills['essential_skills'].apply(lambda x: ','.join(str(x).split('; ')))
       full_occupations_skills['optional_skills'] = full_occupations_skills['optional_skills'].apply(lambda x: ','.join(str(x).split('; ')))
       
       full_occupations_skills_clean = pd.DataFrame({'occupations_skillset': full_occupations_skills['essential_skills']})
       l=[]
       spliskills=full_occupations_skills_clean['occupations_skillset'].str.split(',').tolist()
       l = [x.strip() for lista in spliskills for x in lista if x]
       self.namesprogramming.append('ibatis')
       self.namesprogramming.extend(["Eclipse", "Java" "J2EE", "HTML", "JSP"," JAX RPC", "JAXB", "CSS3", "JavaScript",  "jQuery", "Spring MVC", "Hibernate"," RESTful web services", "Apache Tomcat", "Cucumber", "Cassandra", "Junit", "Jenkins", "Maven", "GitHub", "XML", "Log4j", "EJB", "MySQL", "Ajax"])
       self.uniqueskills=list(set(l))
       self.nlpRemove = spacy.load("it_core_news_lg")
      
         
       self.model = fasttext.load_model(self.pathmodel)
      
       self.namesprogramming.remove('p')
       self. namesprogramming.remove('J')
       self.namesprogramming.remove('G')
       self.namesprogramming.remove('es')
       self.namesprogramming.remove('FL')
       self.namesprogramming.remove('Io')
       self.namesprogramming.remove('K')
       with open(os.path.join(os.getcwd(), "dataset", 'namesCompany.txt'),encoding="utf8") as f:
            self.linescompany = [i.replace('\n',' ').lower() for i in f.readlines() if len(i)>4]
  


   def extract_company(self,text):
     text=text.replace(':','').lower().strip()
     
     comp='non trovata'
     company = re.search("\w+(?=\s(s.p.a.|s.r.l|scarl|ss|snc|sas|spa|srl|srls|sapa|sas|saa|socsoop|s.s|s.n.c|s.a.s|s.p.a|s.r.l|s.r.l.s|s.a.p.a|s.a.s|s.a.a.|soc.coop))", text)
     if company:
           
                   
              
                 start=company.span()[0]
                 end=company.span()[1]
                 compa=text[start:end]
                 if len(compa)>3:
                    comp=text[start:end]
                  
                    
     return comp
            
         
     # else:
     #       Comp='non trovata'
     #       for s in  self.linescompany:
           
     #              span_list = [(match.start(), match.end()) for match in
     #                           re.finditer(fr"\b{s}\b", text)]
     #              if   span_list:
              
     #                  Comp=s
     #                  return Comp
     #                  break 

   def extract_name(self,text):
       with open(os.path.join(os.getcwd(), "dataset", 'NomiCognomi.txt'),encoding="utf8") as f:
           linesnames = [i.replace('\n',' ').title() for i in f.readlines() ]
       text=text.replace(':','').title().strip()
       NAME = re.findall("((Curriculum Vitae|Informazioni Personali|Nome|Cognome|Nome e Cognome) ([A-Z].?\s?)*([A-Z][a-z]+\s?)+)|(([A-Z].?\s?)*([A-Z][a-z]+\s?)+(Curriculum vitae|Informazioni Personali|Nome|Cognome))", text)

       if NAME:
           try:
               if "@" in NAME[0][0]:
                   name=NAME[0][0][-1].split("@")[0].replace('Curriculum Vitae',' ').replace('Informazioni Personali',' ').replace('Cognome',' ').replace('Nome',' ')
               else:
                 name= NAME[0][0].replace('Curriculum Vitae',' ').replace('Informazioni Personali',' ').replace('Cognome',' ').replace('Nome',' ')
               return name
           except IndexError:
               return -1
       else:
           for s in linesnames:
                      
                    
                       span_list = [(match.start(), match.end()) for match in
                                     re.finditer(fr"\b{s.strip()}\b", text.title().strip())]
                      
                       if span_list and len(text.split())<=4:
                           print('NAME',text)
                           return text
         
   def extract_address(self,text,last):
        '''
        Helper function to extract email id from text

        :param text: plain text extracted from resume file
        '''
        text=text.replace(':','').lower().replace('\n','').replace('cap.','').replace('n.','').replace(',','')
        text=re.sub(r'[0-9\n]', '', text.strip().lower()).replace(" ", " ").replace('n°','').replace('–','')
        text=" ".join(text.split())
        address = re.findall("((corso,residenza|luogo di nascita|domicilio|via|viale|piazza|vicolo|piazzale|viale|contrada|circonvallazione) ([a-z].?\s?)*([a-z][a-z]+\s?)+)", text)
      
       
        if address:
            try:
                return address[0][0]
            except IndexError:
                return -1   

   def extract_email(self,text):
       '''
       Helper function to extract email id from text

       :param text: plain text extracted from resume file
       '''
       text=text.replace(':','')
       email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
       if email:
           try:
               return email[0].split()[0].strip(';')
           except IndexError:
               return -1
   def extract_date(self,text,last):
       '''
       Helper function to extract email id from text

       :param text: plain text extracted from resume file
       '''
       text=text.replace(':','').lower().strip()
       data = re.findall("(((\d{1,4}([.\-/])([.\-/])\d{1,4}\s)(nascita|nata|data di nascita|nato|nascita|di nascita))|(\d{1,4}\s(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s\d{1,4})|(nascita|nata|data di nascita|nato|di nascita) ((\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4}))|(nascita|nata|data di nascita|nato|di nascita) ((\s\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})))", text)
      
       if data:
           try:
               return data[0][0]
           except IndexError:
               return -1
       else:
           for s in ["nascita","nata","data di nascita","nato",'nascita','luogo di nascita','di nascita']:
                     
                   
                       span_list = [(match.start(), match.end()) for match in
                                   re.finditer(fr"\b{s}\b", last.lower())]
                       span_list2 =  [(match.start(), match.end()) for match in
                                   re.finditer(fr"\b{s}\b", text.lower())]
                       data = re.findall("(((\d{1,4}([.\-/])([.\-/])\d{1,4}\s))|((\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4}))| ((\s\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})))", text)
                       if  data and len(span_list)>0 and len(span_list2)==0:
                           print('data', text)
                           return text



  
   def convert(self,fname):
       pagenums = set();
       
       manager = PDFResourceManager()
       codec = 'utf-8'
       caching = True
    
     
       output = io.BytesIO()
       converter = HTMLConverter(manager, output, codec=codec, laparams=LAParams())
    
       interpreter = PDFPageInterpreter(manager, converter)  
       infile = open(fname, 'rb')
     #  print("fname...",fname)
       for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=False):
           interpreter.process_page(page)
    
       convertedPDF = output.getvalue()  
    
       infile.close(); converter.close(); output.close()
       return convertedPDF

      
   def ita_estrcation_jobs(self,sentece)  :
        tipojob=[]
        print("START extractjobb")
    
        # len(tipojob) ==0 and  
   
        if   ('assegnista' not in sentece and 'lavoro' not in sentece and 'ricercatore' not in sentece):
          for study in ['diploma','corso formazione','liceo','corso aggiornamneto', 'attestato conseguito','stage','borsista','laurea', 'certificazione','tirocinio','facolatà','facolata','scuola','università','liceo','diploma','dottorato','master','istituto technico']: #corso
              span_list = [(match.start(), match.end()) for match in
                       re.finditer(fr"\b{study}\b",sentece )]
              if span_list and study not in tipojob :
                  tipojob.append(study)
                 
                
    
                  break  
        if len(tipojob) ==0 :
         for idx,job in enumerate(self.listjob):
       
            span_list = [(match.start(), match.end()) for match in
                       
                      re.finditer(fr"\b{job}\b",sentece )]
            if span_list and job not in tipojob:
                tipojob.append(job)
                # print(job)
        
             
     

           
        print("END extractjobb")
        
       
        return tipojob



      
   def extract_skills_npl(self,resume_sections,listacompetenze,worddelete):

       unionskills=[]   
       skillmach=[]
       
       print("START extract_skills_npl")
    
       for testskill in resume_sections:
    
        span_list=[]
        for competenze in listacompetenze: #[ ,'responsabile della','acquisito esperienza','acquisito una collaudata esperienza',
             mach=[(match.start(), match.end()) for match in
                        re.finditer(fr"\b{competenze}\b", testskill)]
             if mach:
                span_list.extend(mach)
               
        if  span_list:  
            if len(testskill)>1:
                
                   for i in range(len(span_list)-1):
                 
                       skillfound=testskill[span_list[i][0]:span_list[i+1][0]]
                       skillmach.append(skillfound ) 
                   skillfound=testskill[span_list[len(span_list)-1][0]:]
                   skillmach.append(skillfound )    
                   if  skillfound.strip()!='' and skillfound not in self.stop and skillfound not in  skillmach and len(skillfound.split())>1 and skillfound not in worddelete:
                      skillmach.append(skillfound.strip() ) #
            else:
               
                if testskill[span_list[0][0]:].strip()!='' and span_list and \
                    testskill[span_list[0][0]:] not in self.stop and testskill not in  skillmach\
                     and len(testskill[span_list[0][0]:].split())>1 and testskill[span_list[0][0]:] \
                         not in worddelete and testskill[span_list[0][0]:] not in skillmach:
                   skillmach.append(testskill[span_list[0][0]:].strip() ) #
       
        #print("testskill",testskill)
        doc = self.nlpRemove(testskill) #clean_txt2(testskill,nlpRemove,stop)
        start=0
        end=0
        verb=[]
        sentece=[]
        endold=0
    
       
        if doc:
            idx=0
    
            for token in doc:
              idx+=1  
          
    
              if token.pos_ == "NOUN" or token.pos_ == "VERB":#  or token.pos_=='DET':
                  start= token.idx  # Start position of token
                  end = token.idx + len(token)  # End position 
                 
                  if token.pos_ == "VERB" : # or token.text in ["conoscenza","competenze","capacità"]:
                     verb.append(token.pos_)
                  
                     # distanza verbo e noun poca al massimo tra verbo e parola ci può stara un adj oa o poco altro 
                
                  if len(verb)>0  and   (-endold +start<= 3 or endold==0) :
    
                      
                      
                      sentece.append( token.text ) # token.text
                      
                      endold= end
                      #oldtoken=token.pos_
                      # se ho 2 verbi sono 2 frrasi e si spezzano
                      if " ".join(sentece).strip()!='' and len(sentece)>=2 and len(verb)>1:
                         sentece.remove( token.text)
                         
                         verbo=verb[-1]
                         verb=[verbo]
                         if len(sentece)>=2:
    
                             unionskills.append(" ".join(sentece))
                         sentece=[ token.text]  #[ token.lemma_]
                       
            if len(verb)==1  and " ".join(sentece).strip()!='' and len(sentece)>1 and " ".join(sentece).strip()!='capacità sono maturate':
                unionskills.append(" ".join(sentece).strip())
       print("END extract_skills_npl")
       return unionskills ,skillmach

   def cosine_similarity(self,v1, v2):
       mag1 = np.linalg.norm(v1)
       mag2 = np.linalg.norm(v2)
       if (not mag1) or (not mag2):
           return 0
       return np.dot(v1, v2) / (mag1 * mag2)
   
   def fasttext_skills(self,unionskills,uniqueskills):
       
      print ("START fasttext_skills")
      candidate_skills_fasttext=[]
      candidate_skills_eco=[]
      for word  in unionskills:
          if len(word.split())<=3:
                threshold=0.75
          else:
              threshold=0.69
          resumes_clean_vec=self.model.get_sentence_vector(word)

          for idx,skills in enumerate(uniqueskills):  #[i for i in row['occupations_skillset'].split(',') ]:
                
                 skills_vec=self.model.get_sentence_vector(skills)
                 
                 score_skill=self.cosine_similarity(skills_vec, resumes_clean_vec)
                 
               
                 if score_skill > threshold and word not in candidate_skills_fasttext:
                                 print( 'word', word, 'skill', skills, score_skill)
                             
                                 candidate_skills_fasttext.append(word)
                                 candidate_skills_eco.append((skills,score_skill))
                                 break
      print("END fasttext_skills")
      return  candidate_skills_fasttext,candidate_skills_eco



  
    
           
   def ita_skills_formsentece(self,frasi):
    

    
        listacompetenze=['skills','addetto al','addetta al','specializzato in','specializzata in',"conoscenza","competenze","capacità",'predisposizione al',"specializzato nell","specializzata nell"]
        worddelete=['capacità e competenze personali','patente guida',"capacità di lettura  capacità di scrittura  capacità di espressione orale","capacità di lettura",  "capacità di scrittura", "capacità di espressione orale", 'capacità di','competenze personali','competenze informatiche','capacità e competenze informatiche','capacità e competenze']
    
        skills,skillmach=  self.extract_skills_npl(frasi,listacompetenze,worddelete)
      
      
        candidate_skills_fasttext,candidate_skills_eco=self.fasttext_skills(skills,self.uniqueskills)
        allskills=candidate_skills_fasttext+skillmach
     
        return  allskills
   def esxtractin_progra_skills(self,frase):
     
      programmingskills=[]
      for s in self.namesprogramming:
                  s = s.replace('+', ' plus').replace('++', 'plus').replace('(',' ').replace(')',' ').replace('* ',' ').replace('+2',' ').strip()
               
                  span_list = [(match.start(), match.end()) for match in
                               re.finditer(fr"\b{s}\b", frase)]
                  if span_list  and s not in programmingskills and s not in ['y)','C','D','T','L','E','F','B','S'] :
                      skill=frase[span_list[0][0]:span_list[0][1]]
                      if skill not in programmingskills:
                       programmingskills.append(s)
      print("end extarct programming skills")
      programmingskillsf=[i for i in programmingskills if i.strip()!='']
      return programmingskillsf
 
   def pdf_to_html(self):
    print("START pdf_to_html")
    filePDF = self.pdfnamepath #("input directory; your pdf file:   ")
    path = os.getcwd()
    fileHTML = os.path.join(path, filePDF + 'dOPUT.html')

    convertedPDF = self.convert(filePDF)
    fileConverted = open(fileHTML, "wb")
    fileConverted.write(convertedPDF)
    fileConverted.close()
    tipojob = []
    index = -1



    all_skills = []





    address = []
    mails_find = []
    name_find = []
    data_nascita = []
    with open(fileHTML, 'r', encoding='utf8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        h4s = soup.find_all('div')
        frasiesperienza = ['0']
        data = []
        frasi = []
        for h4 in h4s:
            frase = []
            for sentece in h4.find_all("span"):
                s = sentece.text.strip()
                if s != '':
                    frase.append(s)

            if frase and frase not in frasiesperienza:

                nestext = " ".join(frase).replace('\n', ' ').strip()
              
                if len([i for i in mails_find if i is not None and i.strip() != '']) == 0:
                    mails_find.append(self.extract_email(nestext.lower()))
                    # name_find.append(mails_find[-1].split("@")[0])
                mail = [i for i in mails_find if i is not None and i.strip() != '']
                if len([i for i in address if i is not None and i.strip() != '']) == 0:
                    address.append(self.extract_address(nestext.lower(), frasiesperienza[-1]))
                if len([i for i in name_find if i is not None and i.strip() != '']) == 0:
                    name_find.append(self.extract_name(nestext.title()))
                if len([i for i in data_nascita if i is not None and i.strip() != '']) == 0:
                    data_nascita.append(self.extract_date(nestext.lower(), frasiesperienza[-1]))
                if len([i for i in name_find if i is not None and i.strip() != '']) == 0 and len(mail) > 0:
                    name_find.append(mail[0].split("@")[0])
                frasiesperienza.append(" ".join(frase))
                index += 1
                pattern = re.compile(r"[;,.] ")
                testo = [re.sub(r'[^\w\s]', '', i.strip().lower()) for i in pattern.split(" ".join(frase)) if
                         re.sub(r'[^\w\s]', '', i.strip()) != '']

                frasi.extend(testo)

                string = " ".join(frase).lower().strip()
                string = string.replace("  ", " ").replace('‘', '')
    

                # solo date mm/dd/yy o con -'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})

                # solo date mm/dd/ o con -  (\d{1,4}([.\-/])\d{1,2}\d{1,4})

                # assieme '(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})|(\d{1,2}([.\-/])\d{1,4})'
                if 'data di nascita' not in frasiesperienza[index - 1].strip().lower() \
                        and 'sesso' not in string \
                        and 'europass' not in string and 'ufficio di collocamento ' not in string \
                        and 'nome' not in string and 'dati personali' not in string \
                        and string not in tipojob and 'data di nascita' not in string \
                        and 'pagina' not in string and 'autorizzo il trattamento' not in string \
                        and 'consenso  al trattamento' not in string and 'hrs' not in string and \
                        'curriculum vitae ' not in string and \
                        'dell’ar' not in string and \
                        'dall’art.' not in string and 'decreto legge' not in string \
                        and ' tel.' not in string and 'cellulare' not in string \
                        and 'patente' not in string and 'nascita' not in string and 'd.lg' not in string \
                        and '© unione europea' not in string and 'curriculum vitae' not in string:

                    matches = search_dates(string, settings={"STRICT_PARSING": True,
                                                             'PARSERS': ['timestamp', 'absolute-time'], },
                                           languages=['it', 'en'])
                    if matches and string not in tipojob:
                        tipojob.append(string)
                        data.append((index, " ".join(frase).lower().strip()))
                      
                    # print(string)
                    if string not in tipojob:
                        x = re.findall(
                            r'((\b\d{1,4} ([-/–]*) (oggi|attuale|in corso|presente|present)\b)|(\b(0|[0-12][0-9])([\-/–])\d{1,2}[0-12]\b)([\-/–])\d{1,4})|(\b(0|[0-12][0-9])([\-/])\d{2,4})|(\b\d{1,4}(\s[-/–]*)(0|[0-12][0-9])(oggi|attuale|in corso|presente|present, fino al)\b)|(\b\d{4}([-–])\d{4})|(\b\d{4}(\s[-–]*)\s\d{4})|(\b\d{4}(\s[al]*)\s\d{4})|(\b\d{1,4}([-/–]*)(0|[0-12][0-9])(oggi|attuale|in corso|presente|present)\b)|(\b\d{1,4}([-/–]*)(oggi|attuale|in corso|presente|present)\b)|((\b\d{1,4}([-/– ]*)(oggi|attuale|in corso|presente|present))\b)(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})',
                            string, re.DOTALL)
                        if x and string not in tipojob:
                    
                            tipojob.append(" ".join(frase).lower().strip())
                            data.append((index, " ".join(frase).lower().strip()))

                        y = re.findall(
                            r'(\d{1,4}\s)(February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sept|September|Oct|October|Nov|November|Dec|December|gennaio|gen.|gen.|febbraio|feb|feb.|mar|mar.|marzo|aprile|apr|apr.|mag.|mag|maggio|giu|giu.|giugno|luglio|lug.|lug|agosto|ago.|ago|set|set.|settembre|ott.|ott|ottobre|nov.|nov|novembre|dicembre|dic.|dic)'
                            , string)
                        if y and string not in tipojob:
                         
                            tipojob.append(" ".join(frase).lower().strip())
                            data.append((index, " ".join(frase).lower().strip()))

                        z = re.findall(
                            r'((\b(February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sept|September|Oct|October|Nov|November|Dec|December|gennaio|gen|febbraio|feb|mar|marzo|aprile|apr|mag|maggio|giu|giugno|luglio|lug|agosto|ago|set|settembre|ott|ottobre|nov|novembre|dicembre|dic)(\s\d{1,4}))) |(\b(February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sept|September|Oct|October|Nov|November|Dec|December|gennaio|gen|febbraio|feb|mar|marzo|aprile|apr|mag|maggio|giu|giugno|luglio|lug|agosto|ago|set|settembre|ott|ottobre|nov|novembre|dicembre|dic) (\d{1,4}))',
                            string)

                        if z and string not in tipojob:
                       
                            tipojob.append(" ".join(frase).lower().strip())
                            data.append((index, " ".join(frase).lower().strip()))

    os.remove(fileHTML)
    print("END pdf_to_html")
    skills = self.ita_skills_formsentece(frasi)
    address_ = [i for i in [address + ["non trovati"]][0] if i != '' and i is not None][0]
    mails_ = [i for i in [mails_find + ["non trovati"]][0] if i != '' and i is not None][0]
    name_ = [i for i in [name_find + ["non trovati"]][0] if i != '' and i is not None][0]
    data_ = [i for i in [data_nascita + ["non trovati"]][0] if i != '' and i is not None][0]

    df0 = pd.DataFrame(
        {'nome e cognome': [name_], 'residenza o domicilio': [address_], 'mails': [mails_], 'data nascita': data_})

    print("start rs")
    all_skills.extend(skills)
    all_skills = list(set(all_skills))
    
    prog = self.esxtractin_progra_skills(' '.join(frasi))
    if prog:
        all_skills.extend(prog)
    test = []

    job = []
    inedx = 0
    frasiesperienza = frasiesperienza[1:]
    # salto l'utima data
    while inedx + 1 < len(data):
        string = ",".join(
            frasiesperienza[data[inedx][0]:data[inedx + 1][0]]).lower().strip()  # len(string.split())>2   and
        string_list = string.split()[0:10]
        if 'data di nascita' not in string_list and ((('© unione europea' not in string_list \
                                                       and 'd.lg' not in string_list and 'europass' not in string_list))):
            test.append(string.replace('\n', ' '))
         
            new_string = re.sub(r'[^\w\s]', ' ', string).replace('\n', ' ')
            jobs =self. ita_estrcation_jobs(new_string)

            category = jobs

    
            job.append(category)
            print("ennd string............")
            # print(inedx,string)
        inedx += 1

    if data[inedx][0] + 4 < len(frasiesperienza) and 'data di nascita' not in ",".join(
            frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip() \
            and 'dell’art.' not in ",".join(
        frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip() and '© unione europea' not in ",".join(
        frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip() \
            and 'd.lg' not in ",".join(
        frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip() and 'europass' not in ",".join(
        frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip():  # and len(data[inedx][1].split())>=2  :
        test.append(",".join(frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip().replace('\n', ' '))

        new_string = re.sub(r'[^\w\s]', '',
                            ",".join(frasiesperienza[data[inedx][0]:data[inedx][0] + 4]).lower().strip())
        jobs =self.ita_estrcation_jobs(new_string)

      
        category = jobs

      
        job.append(category)
    else:
        if 'dell’art.' not in frasiesperienza[data[inedx][0]] and 'data di nascita' not in frasiesperienza[
            data[inedx][0]] and '© unione europea' not in frasiesperienza[data[inedx][0]] \
                and 'd.lg' not in frasiesperienza[data[inedx][0]] \
                and 'europass' not in frasiesperienza[data[inedx][0]]:
            test.append(frasiesperienza[data[inedx][0]].lower().strip().replace('\n', ' '))
            new_string = re.sub(r'[^\w\s]', '', frasiesperienza[data[inedx][0]].lower().strip())
            jobs = self.ita_estrcation_jobs(new_string)


            category = jobs

            job.append(category)

    preprocessing = JobPostsProcessing()
    it_job_posts = preprocessing.processed_dataset
    # it_job_posts['jobTitle'] = it_job_posts['jobTitle'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip().lower())
    it_job_posts['jobDescription'] = it_job_posts['jobDescription'].apply(lambda x: re.sub(r'[^\w\s]', '', x).strip().lower().replace(',',''))
    description = it_job_posts['jobDescription'].tolist()
  

    it_job_posts["Domain"] = it_job_posts[['jobDescription', "jobTitle"]].apply(lambda x: ", ".join(x), axis=1)

   
    rs = pd.DataFrame(
        columns=['job user', 'company user','jobID', 'jobCompany', 'jobTitle', 'scoreFinal', 'scoreDom', 'scoreSkills', 'scoreTime'])

    jobslist = it_job_posts['jobTitle'].tolist()
    
    exp = [experience for experience in job if
           " ".join(experience) not in ['corso formazione', 'corso', 'attestato conseguito', 'stage', 'laurea',
                                        'facoltà', 'facolta', 'scuola', 'università', 'liceo', 'diploma', 'dottorato',
                                        'master', 'istituto technico'] and len(experience) > 0]
    scortime = 1 / len(exp)
    count = len(exp)


    company=[]
  
   
    
    score_skills1 = np.array(FeatureExtraction.TFIDF(description, [" ".join(all_skills).replace('\n', '')]))
    score_skills = list((score_skills1 - score_skills1.min()) / (score_skills1.max() - score_skills1.min()))
    for experience, text in zip(job, test):
     
        if len(experience) > 0 and ",".join(experience) not in ['corso formazione', 'corso', 'attestato conseguito',
                                                                'stage', 'laurea', 'facoltà', 'facolta', 'scuola',
                                                                'università', 'liceo', 'diploma', 'dottorato', 'master',
                                                                'istituto technico']:
            scortime1 = scortime * count

           
            company=self.extract_company(text)
            scoreDomin1 = np.array(
                FeatureExtraction.TFIDF(description, [" ".join(experience).replace('\n', ' ') + text.replace('\n', ' ')]))
            scoreDomin = (scoreDomin1 - scoreDomin1.min()) / (scoreDomin1.max() - scoreDomin1.min())
            #

       
            output_tfidf = (((scoreDomin * scortime1)) + np.array(score_skills)) / 2
            top = sorted(range(len(output_tfidf)), key=lambda i: output_tfidf[i], reverse=True)[:1]
            list_scores = [output_tfidf[i] for i in top]
            list_scoreDomin = [scoreDomin[i] for i in top]
            list_score_skills = [score_skills[i] for i in top]
            list_score_time = [scortime1 for i in top]
            rs = rs.append(
                CrossFunctions.get_recommendation(top, it_job_posts, list_scores, experience, list_scoreDomin,
                                                  list_score_skills, list_score_time,company))

        
         
            description.pop(jobslist.index(rs.iloc[-1].jobTitle))
            score_skills.pop(jobslist.index(rs.iloc[-1].jobTitle))

            count = count - 1

           

   
  
    df = pd.DataFrame({'name': test, 'jobTitke': job})

    df= df[df['jobTitke'].map(lambda d: len(d)) > 0]

    with pd.ExcelWriter(self.folder, engine='xlsxwriter') as writer1:
        # df.to_excel(name,index=False)
        df.to_excel(writer1, sheet_name='job titles', index=False)
        df0.to_excel(writer1, sheet_name='informazioni personali', index=False)
        df1 = pd.DataFrame({"allskills": all_skills})
        rs.to_excel(writer1, sheet_name='RS lavori', index=False)
        df1.dropna(subset=['allskills'], inplace=True)

        filter = df1["allskills"] != ""
        dfNew = df1[filter]
        dfNew.to_excel(writer1, sheet_name='allskills', index=False)
    writer1.save()
    print('END rs')

    return rs
   



          
    










 







