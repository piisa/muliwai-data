#Create synthetic PII dataset from different domains
from datasets import load_dataset
import os
import re
import itertools
from re import finditer
import glob
import random
from .names import *

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def stem(s):
  s = s.replace(".", " ").replace("!", " ").replace("?", " ").replace(",", " ").replace("-", " ").replace(";", " ").replace("'", " '").replace("\"", " \"")
  sArr = s.lower().split()
  if len(sArr) > 4:
    sArr = sArr[:4]
  s = " ".join([s1[:4] if len(s1) > 4 else s1 for s1 in sArr if s1.strip()])
  return s

def has_any(s, lst):
  for l in lst:
    if l in s: return True
  return False


#Create synethic PII dataset that is not domain specific
from datasets import load_dataset
import os
import re
import itertools
from re import finditer
import glob
import random
from .names import *
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def stem(s):
  s = s.replace(".", " ").replace("!", " ").replace("?", " ").replace(",", " ").replace("-", " ").replace(";", " ").replace("'", " '").replace("\"", " \"")
  sArr = s.lower().split()
  if len(sArr) > 4:
    sArr = sArr[:4]
  s = " ".join([s1[:4] if len(s1) > 4 else s1 for s1 in sArr if s1.strip()])
  return s

def save_enron_line(l2, prev, o):
        l2 = remove_html_tags(l2)
        l2 = l2.split('-----Original Message-----')[0].strip()
        l2 = l2.split('---------------------- Forwarded')[0].strip()
        l2 = l2.split('----- Forwarded')[0].strip()
        l2 = l2.split('---------From:')[0].strip()
        l2 = l2.split('**********************************************************************This')[0].strip()
        l2 = l2.split('**********************************************************************   This')[0].strip()
        l2 = l2.split('******************************************************************This')[0].strip()
        l2 = l2.split('*************************************************This')[0].strip()
        l2 = l2.split('********************************************************************** This')[0].strip()
        l2 = l2.split('--------- Inline attachment follows')[0].strip()
        l2 = l2.split('The information contained in this e-mail message and')[0].strip()
        l2 = l2.split('This message is for the designated recipient')[0].strip()
        l2 = l2.split('***Please be advised')[0].strip()
        l2 = l2.split('*******This message')[0].strip()
        l2 = l2.split('This message (including any attachments) contains')[0].strip()
        l2 = l2.split('*********************************************************')[0].strip()
        l2 = l2.split('_________________________________________________________________Get')[0].strip()
        l2 = l2.split('___________________________________________')[0].strip()
        l2 = l2.split('__________________________________________________ Do')[0].strip()
        l2 = l2.replace("\\\"", " \" ").replace("(", " (").replace(")", ") ").replace("[", " [").replace("]", "] ").replace("?", "? ").replace("!", "! ").replace("? ?", "??").replace("! !", "!!").replace(":", ": ").replace("\t", " ").replace("= ", "").replace("=20","").replace("=90","").replace("=018","").replace("=09","").replace("=3D","")
        l2 = l2.replace(" s ", " 's ").replace(" ve ", " 've ").replace(" re ", " 're ").replace(" ll ", " 'll ").replace(" m ", " 'm ").replace(" t ", " 't ").replace(" d ", " 'd ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace(". . .", "...")
        l2 = l2.replace(". yahoo", ".yahoo").replace("www. ", "www.").replace(". htm", ".htm").replace(". co", ".co").replace(". org", ".org").replace(". edu", ".edu").replace(". net", ".net").replace(". NET", ".NET").replace(". CO", ".CO").replace(". ORG", ".ORG").replace(". EDU", ".EDU").replace(": //", "://")
        l2 = l2.replace(": 0", ":0").replace(": 1", ":1").replace(": 2", ":2").replace(": 3", ":3").replace(": 4", ":4").replace(": 5", ":5").replace(": 6", ":6").replace(": 7", ":7").replace(": 8", ":8").replace(": 9", ":9")
        l2 = l2.replace(". url -", ".url - <<").replace(". doc -", ".doc - <<").replace(". pdf -", ".pdf <<").replace(". xls -", ".xls <<").replace(". url", ".url>>").replace(". doc", ".doc>>").replace(". pdf", ".pdf>>").replace(". xls", ".xls>>").replace("<< ", "<<").replace("> >", " ").replace("  ", " ")
        l2 = l2.replace(". URL -", ".URL - <<").replace(". DOC -", ".DOC - <<").replace(". PDF -", ".PDF <<").replace(". XLS -", ".xls <<").replace(". URL", ".URL>>").replace(". DOC", ".DOC>>").replace(". PDF", ".PDF>>").replace(". XLS", ".XLS>>").replace("<< ", "<<").replace("> >", " ").replace("  ", " ")
        l2 = l2.replace("RE:", "").replace("Re:", "").replace("RE: ", "").replace("Re: ", "").replace("Fw: ", "").replace("FW: ", "").replace("FWD: ", "").replace("Fwd: ", "")
        l2 = l2.replace('Importance: High',':')
        if "Sent:" in l2: return
        l2 = l2.replace("...", "... ").replace("\"\"", " \" ").replace("  ", " ").strip(" -:;[]()\=<>\"").rstrip(".!?")
        l2Arr = l2.split()
        if len(l2Arr) > 3:
          l2 = " ".join(itertools.chain(*[camel_case_split(a) for a in l2Arr]))
          if l2.replace(":", "").replace("[", "").replace("]", "").replace(".", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace(";", "").replace(" ", "").lower() in prev: return
          l2 = l2.replace("==", "--")
          l2 = l2.replace("++", "--")
          l2 = l2.replace("*~", "--")
          l2 = l2.replace("||", "--")
          l2 = l2.replace("**", "--")
          l2 = l2.replace("__", "--")
          l2 = l2.replace("##", "--")
          for l3 in l2.split('--'):
            l3 = l3.strip()
            if l3:
              for l4 in l3.split("Subject: "):
                l4 = l4.strip('=, ')
                if l4: o.write(l4+"\tenron\n")
          prev[l2.replace(":", "").replace("[", "").replace("]", "").replace(".", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace(";", "").replace(" ", "").lower()] = 1

def has_any(s, lst):
  for l in lst:
    if l in s: return True
  return False

     
def create_cleaned_combined(share_di):   

  """
  Creates a combined English dataset from different domains useful for doing PII detection. 
  
  Domains include enron (email), newspop (social media),  casehold (legal), mtsamples (medical), excerpts from a few contrats from the SEC govt website,  
    financial_phrasebank (business), banking 77 (financial), PII examples from Presidio (generic), civil comments (social media) 
  Do some deduplication and cleanup. 
  Add some PII as augumentation (TBD: some {PERSON} and {ORG} tags added. Need to add some more categories).

  See specific licenses for each dataset. 
  """    
  

  prev={}
  if not os.path.exists("cleaned_combined_pii.tsv"):
    with open("combined.tsv", "w", encoding="utf8") as o:

      """
     @article{Moniz2018MultiSourceSF,
  title={Multi-Source Social Feedback of Online News Feeds},
  author={N. Moniz and L. Torgo},
  journal={ArXiv},
  year={2018},
  volume={abs/1801.07055}
    }   
      """
             
        
      #https://huggingface.co/datasets/newspop#licensing-information - CC-BY
      #download using datasets and use
      dataset = load_dataset("newspop")
      topics_to_ner = {'economy':None, 'microsoft': '{ORG}', 'obama': '{PUBLIC_FIGURE}', 'palestine': '{GPE}'}
      for d in (dataset['train'], ):
        for idx, data in enumerate(d):
          l2, headline, topic = data['title'], data['headline'], data['topic']
          ner_label = topics_to_ner.get(topic)

 
   
      #https://huggingface.co/datasets/banking77 under CC-by-4.0
      """
      @inproceedings{Casanueva2020,
    author      = {I{\~{n}}igo Casanueva and Tadas Temcinas and Daniela Gerz and Matthew Henderson and Ivan Vulic},
    title       = {Efficient Intent Detection with Dual Sentence Encoders},
    year        = {2020},
    month       = {mar},
    note        = {Data available at https://github.com/PolyAI-LDN/task-specific-datasets},
    url         = {https://arxiv.org/abs/2003.04807},
    booktitle   = {Proceedings of the 2nd Workshop on NLP for ConvAI - ACL 2020}
    }
      """
      dataset = load_dataset("banking77")
      for d in (dataset['train'], ):
        for idx, data in enumerate(d):
          l2 = data['text']
          l2 = l2.replace("\n", " ").replace("  ", " ").replace("  ", " ")
          l2Arr = l2.split()
          if len(l2Arr) > 3:
            l2 = l2.replace("bank account", "{FINANCIAL_PRODUCT} account").replace("card", "{FINANCIAL_PRODUCT}").replace("Google Pay", "{ORG} {FINANCIAL_PRODUCT}").replace("Apple pay", "{ORG} {FINANCIAL_PRODUCT}").replace("American Express", "{FINANCIAL_PRODUCT}")
            l2 = l2.replace("Apple Watch", "{DEVICE}")
            l2 = l2.replace("US", "{GPE}").replace("EU", "{GPE}").replace("UK", "{GPE}").replace("European Union", "{GPE}").replace("Europe", "{GPE}")
            if l2.startswith("Why"): continue
            if (" id " in l2 or "ident" in l2):
              o.write (l2+random.choice([" My id is {ID}.", " SSN: {ID}.", " My number is {ID}."])+"\tbanking77\n")
            elif "get " in l2 or "order " in l2 or "like " in l2 or "want " in l2:
              if random.choice([0,1]):
                o.write (random.choice(["My name is {PERSON}, DOB: {DATE}. ", "{PERSON} here. ", "I'm {PERSON}. "])+ l2+"\tbanking77\n")
              else:
                o.write (l2.strip(' ?.') + random.choice(["? My name is {PERSON}.", "? {PERSON} here.", "? I'm {PERSON}."])+"\tbanking77\n")
            else:
              o.write (l2.strip(' ?.') + random.choice(["? Acct #: {CARDINAL}.", "? My name is {PERSON}, DOB: {DATE}, Acct #: {CARDINAL}.", "? Asking for acct #: {CARDINAL}.", "? My name is {PERSON}, DOB: {DATE}"])+"\tbanking77\n")


      #https://github.com/reglab/casehold court cases are government works and in the public domain. annotations and selections are under  Apache-2.0 License
      """
      @inproceedings{zhengguha2021,
	title={When Does Pretraining Help? Assessing Self-Supervised Learning for Law and the CaseHOLD Dataset},
	author={Lucia Zheng and Neel Guha and Brandon R. Anderson and Peter Henderson and Daniel E. Ho},
	year={2021},
	eprint={2104.08671},
	archivePrefix={arXiv},
	primaryClass={cs.CL},
	booktitle={Proceedings of the 18th International Conference on Artificial Intelligence and Law},
	publisher={Association for Computing Machinery}
  }      
      """
      with open(f"{share_dir}/casehold.csv", "rb") as f:
        while True:
          line = f.readline().decode()
          if not line: break
          line = line.split(",\"")
          if len(line) >= 2:
            line = line[1]
            line = line.split("(<HOLDING>)")
            if len(line) == 2:
              s1, s2 = line
              s1 = s1.replace("  ", " ").replace("  ", " ")
              s2 = s2.replace("  ", " ").replace("  ", " ")
              s2 = ' '.join(s2.split(',')[:-6]).strip(';: ')
              if s2:
                o.write(s1+' HOLDING: '+s2+"\tcasehold\n")
              else:
                o.write(s1+"\tcasehold\n")
            else:
              s1 = s1.replace("  ", " ").replace("  ", " ")
              o.write(s1+"\tcasehold\n")


      #from https://www.kaggle.com/wcukierski/enron-email-dataset, originally from https://www.cs.cmu.edu/~enron/ 
      # public data and partially copyrighted works (annotations) used by permission of authors
      """
      Public record data origially published by www.ferc.gov. Subsequent data cleansing by the authors and released
      "as a resource for researchers who are interested in improving current email tools, or understanding how email is currently used". 
      """
      with open(f"{share_dir}/kaggle_enron_emails.csv", "rb") as f:
        in_message = False
        l2 = ""
        while True:
          l = f.readline()
          if not l: break
          l = l.decode().strip()
          if not in_message and l.startswith("Subject:"):
            l = l.replace("Subject:", "").strip()
            if l: l2 = l+ ":"
          if "X-FileName" in l:
            in_message = True
            continue
          elif "Message-ID" in l:
            save_enron_line(l2, prev, o)
            l2 = ""
            in_message = False
          if in_message:
            l2 += " "+l
            
        if l2:
          save_enron_line(l2, prev, o)
  
      #https://huggingface.co/datasets/civil_comments - CC0
      """
      @article{DBLP:journals/corr/abs-1903-04561,
  author    = {Daniel Borkan and
               Lucas Dixon and
               Jeffrey Sorensen and
               Nithum Thain and
               Lucy Vasserman},
  title     = {Nuanced Metrics for Measuring Unintended Bias with Real Data for Text
               Classification},
  journal   = {CoRR},
  volume    = {abs/1903.04561},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.04561},
  archivePrefix = {arXiv},
  eprint    = {1903.04561},
  timestamp = {Sun, 31 Mar 2019 19:01:24 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1903-04561},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
      """
      dataset = load_dataset("civil_comments")
      for d in (dataset['train'], ):
         for idx, data in enumerate(d):
          score = sum ([data[feature] for feature in [ 'toxicity', 'severe_toxicity', 'obscene', 'threat', 'insult', 'identity_attack', 'sexual_explicit']])
          l2 = data['text']
          l2 = l2.replace("Trump","{PUBLIC_FIGURE}").replace("Trump","{PUBLIC_FIGURE}").replace("Obama","{PUBLIC_FIGURE}").replace("Clinton","{PUBLIC_FIGURE}").replace("Trudeau","{PUBLIC_FIGURE}")
          l2 = l2.replace('Alaskans', '{NORP}').replace('Alaskan', '{NORP}').replace('Alaska', '{GPE}').replace('Americans', '{NORP}').replace('American', '{NORP}').replace('America', '{GPE}').replace('Oregon', '{GPE}').replace('United States', '{GPE}').replace('Seattle','GPE')
          l2 = l2.replace("\n", " ").replace("  ", " ").replace("  ", " ")
          l2Arr = l2.split()
          has_a_name = has_any(first_names, l2Arr)
          l2_lower = l2.lower()
          if random.choice([0,1]) and not has_a_name and "mr." not in l2_lower and "ms." not in l2_lower and  "mrs." not in l2_lower and "president" not in l2_lower and "governor" not in l2_lower and  "mayor" not in l2_lower:
            continue
          l2 = " ".join(["{DOMAIN_NAME}" if a.startswith("http") or a.startswith("www") else a for a in l2Arr])
          if len(l2Arr) > 10 and len(l2Arr) < 50 and (score <= 0.5 or random.randint(0, 10)==0): # having too much toxic content may skew the data
            if has_a_name or "mr." in l2_lower or "ms." in l2_lower or "mrs." in l2_lower or "president" in l2_lower or "governor" in l2_lower or "mayor" in l2_lower:
              o.write (l2+"\tcivil_comments\n")
            elif "you " in l2_lower and random.choice([0,1]):
              if l2.startswith("you"):
                l2 = l2.replace("you ", "{PERSON} you ", 1)
                o.write (l2+"\tcivil_comments\n")
              elif l2.startswith("You"):
                l2 = l2.replace("You ", "{PERSON} you ", 1)
                o.write (l2+"\tcivil_comments\n")

      #Download data using datasets from here https://huggingface.co/datasets/financial_phrasebank and put in to share_dir
      for file in glob.glob(f"{share_dir}/FinancialPhraseBank-v.10/*"):
        with open(file, "rb") as f:
          while True:
            l2 = f.readline().decode()
            if not l2: break
            l2 = l2.replace("\n", " ").replace("  ", " ").replace("  ", " ")
            l2 = l2.replace("Finland", "{GPE}")
            l2 = l2.replace("Finnish", "{NORP}")
            l2Arr = l2.split()
            if len(l2Arr) > 3:
              l2_lower = l2.lower()
              need_processing=True
              say_words = ["said", "stated", "remarked", "wrote", "announced", "acknowledged"]
              for say in say_words:
                if say not in l2_lower: continue
                if random.randint(0, 1)==0: 
                  need_processing=False
                  continue
                need_processing=False
                l2 = l2.replace(f"also {say}", say)
                l2 = l2.replace(f"further {say}", say)
                if f"she {say}" in l2_lower:
                  l2 = l2.replace(f"she {say}", f"{PERSON} {say}")
                elif f"he {say}" in l2_lower:
                  l2 = l2.replace(f"he {say}", f"{PERSON} {say}")
                elif f", {say}" not in l2_lower and f"'' {say}" not in l2_lower:
                  if has_any(first_names, l2Arr) or "mr" in l2_lower or "mrs" in l2_lower or "ms" in l2_lower or "ceo" in l2_lower or "manager" in l2_lower or "director" in l2_lower:
                    if random.randint(0, 10)==0:
                      l2 = l2.replace(say, random.choice(["'s spokeswoman {PERSON} "+say, "'s spokesman {PERSON} "+say, f"'s spokesperson {PERSON} "+say]))
                  else:
                    l2 = l2.replace(say, random.choice(["'s spokeswoman {PERSON} "+say, "'s spokesman {PERSON} "+say, f"'s spokesperson {PERSON} "+say]))
                #print (l2)
              if need_processing:
                if has_any(first_names, l2Arr) or"mr" in l2_lower or "mrs" in l2_lower or "ms" in l2_lower or "ceo" in l2_lower or "manager" in l2_lower or "director" in l2_lower:
                    if random.randint(0, 10)==0:
                      l2= (l2.strip(" .") + random.choice([" according to company spokesperson {PERSON}", " said spokesman {PERSON}", ", said company spokeswoman {PERSON}", ", acknowledged {ORG}'s {PERSON}", ", reiterated {PERSON}",]))
                else:
                  if random.choice([0,1]):
                    l2= (l2.strip(" .") + random.choice([" according to spokesperson {PERSON}", ", said company spokesman {PERSON}", " said spokeswoman {PERSON}", ", acknowledged {PERSON}", ", reiterated {ORG} CEO {PERSON}", " said Ms. {PERSON}", ", said Mr. {PERSON}",  ", stated Ms. {PERSON}", " stated Mr. {PERSON}"]))
                  else:
                    l2= (random.choice(["According to {ORG} spokesperson {PERSON}, ", "Said company spokesperson {PERSON}, ", "Said CEO {PERSON}, ", "Chairwoman {PERSON}: ","{PERSON} stated: "])+ l2)
              o.write (l2+"\tfinancial_phrasebank\n")
              
      #from mtsmples.  https://www.kaggle.com/tboyle10/medicaltranscriptions#mtsamples.csv.  see https://www.mtsamples.com/ 
      #download data and put into share_dir
      #"Please feel free to print, share, link, and distribute any of the reports from our website. Our requirement is that while linking or sharing or printing, please notify us, and please give credit to our web site by putting a link to https://www.mtsamples.com or putting a referral note regarding www.mtsamples.com
      with open(f"{share_dir}/mtsamples.csv", "rb") as f:
        while True:
          line = f.readline().decode()
          if not line: break
          line = line.strip()
          line = line.split(",",1)[1]
          lineArr = line.split('","', 2)
          arr = []
          if len(lineArr) == 2:
            text, keywords =  lineArr
            text1, text2, text3 = text.strip(' "').split(',', 2)
            arr.append(text1)
            if ',"' in text3:
              text3Arr = text3.split(',"')
              if len(text3Arr[0]) < 20:
                text3 = text3Arr[1]
            for s in  text3.strip(' "').split(".,"):
              s = s.strip().replace(":,",": ").replace(": ,",": ").replace(":  ,", ": ").replace(",", ", ").replace("  ", " ").replace("  ", " ")
              for s2 in s.split(",\""):
                arr.append (s2.strip(' .'))
            #print (keywords.strip().split(","))
            l = '. '.join(arr).replace(', "', '. ').replace('",', ' ').replace("..",".").replace('.  .','. ').replace(' .','.').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
            if 'ABCD' in l:
              l = l.replace("ABCD", "{ORG}")
            if 'MM/DD/YYYY' in l:
              l = l.replace('MM/DD/YYYY', '{DATE}')
            if 'ABC' in l:
              l = l.replace("ABC", '{PERSON}')
            if 'Mr. A' in l:
              l = l.replace("Mr. A", 'Mr. {PERSON_5}')
            if 'Ms. A' in l:
              l = l.replace("Ms. A", 'Ms. {PERSON_5}')
            if 'XYZ' in l:
              l = l.replace("XYZ", '{PERSON_2}')
            if 'XXXX' in l:
              l = l.replace("XXXX", '{PERSON_3}')
            if 'Ms. X' in l:
              l = l.replace("Ms. X", 'Ms. {PERSON_4}')
            if 'Mr. X' in l:
              l = l.replace("Mr. X", 'Mr. {PERSON_4}')
            if 'Dr. X' in l:
              l = l.replace("Dr. X", 'Dr. {PERSON_3}')
            if '{PERSON} Avenue' in l:
              l = l.replace('{PERSON} Avenue', '{ADDRESS}')
            if 'at {PERSON_1}' in l: 
              l = l.replace('at {PERSON_1}', 'at {LOC}')
            if 'in {PERSON_1}' in l:
              l = l.replace('in {PERSON_1}', 'in {LOC}')
            if 'at {PERSON_2}' in l: 
              l = l.replace('at {PERSON_2}', 'at {LOC}')
            if 'in {PERSON_2}' in l:
              l = l.replace('in {PERSON_2}', 'in {LOC}')
            if 'at {PERSON_3}' in l: 
              l = l.replace('at {PERSON_3}', 'at {LOC}')
            if 'in {PERSON_3}' in l:
              l = l.replace('in {PERSON_3}', 'in {LOC}')
            if 'at {PERSON_4}' in l: 
              l = l.replace('at {PERSON_4}', 'at {LOC}')
            if 'in {PERSON_4}' in l:
              l = l.replace('in {PERSON4_}', 'in {LOC}')
            
            if '{PERSON_2} County' in l:
              l = l.replace('{PERSON_2} County', '{ORG_2} County')
            #MR#
            l = l.strip(' "')
            o.write(l+"\tmtsamples\n") 

   
      #https://huggingface.co/datasets/banking77
      #Download data using datasets and put into the share_dir
      dataset = load_dataset("banking77")
      for d in (dataset['train'], ):
        for idx, data in enumerate(d):
          l2 = data['text']
          l2 = l2.replace("\n", " ").replace("  ", " ").replace("  ", " ")
          l2Arr = l2.split()
          if len(l2Arr) > 3:
            l2 = l2.replace("bank account", "account").replace("Google Pay", "{ORG} account").replace("Apple pay", "{ORG} account").replace("American Express", "{ORG} account")
            l2 = l2.replace("Apple Watch", "device")
            l2 = l2.replace("US", "{GPE}").replace("EU", "{GPE}").replace("UK", "{GPE}").replace("European Union", "{GPE}").replace("Europe", "{GPE}")
            if l2.startswith("Why"): continue
            if (" id " in l2 or "ident" in l2):
              o.write (l2+random.choice([" My id is {ID}.", " SSN: {ID}.", " My number is {ID}."])+"\tbanking77\n")
            elif "get " in l2 or "order " in l2 or "like " in l2 or "want " in l2:
              if random.choice([0,1]):
                o.write (random.choice(["My name is {PERSON}, DOB: {DATE}. ", "{PERSON} here. ", "I'm {PERSON}. "])+ l2+"\tbanking77\n")
              else:
                o.write (l2.strip(' ?.') + random.choice(["? My name is {PERSON}.", "? {PERSON} here.", "? I'm {PERSON}."])+"\tbanking77\n")
            else:
              o.write (l2.strip(' ?.') + random.choice(["? My name is {PERSON}, DOB: {DATE}, Acct #: {ID}.", "? Asking for acct #: {ID}.", "? My name is {PERSON}, DOB: {DATE}, Acct #: {ID}."])+"\tbanking77\n")


      #https://github.com/reglab/casehold
      #Download data using datasets and put into the share_dir
      
      with open(f"{share_dir}/casehold.csv", "rb") as f:
        while True:
          line = f.readline().decode()
          if not line: break
          line = line.split(",\"")
          if len(line) >= 2:
            line = line[1]
            line = line.split("(<HOLDING>)")
            if len(line) == 2:
              s1, s2 = line
              s1 = s1.replace("  ", " ").replace("  ", " ")
              s2 = s2.replace("  ", " ").replace("  ", " ")
              s2 = ' '.join(s2.split(',')[:-6]).strip(';: ')
              if s2:
                o.write(s1+' HOLDING: '+s2+"\tcasehold\n")
              else:
                o.write(s1+"\tcasehold\n")
            else:
              s1 = s1.replace("  ", " ").replace("  ", " ")
              o.write(s1+"\tcasehold\n")


      #https://huggingface.co/datasets/medical_dialog
      #and https://github.com/UCSD-AI4H/COVID-Dialogue from the same authors
      #Download data using datasets and put into the share_dir
      
      files = glob.glob(f"{share_dir}/Medical-Dialogue-Dataset-English-COVID/*")
      all_lines = []
      for file in files:
          with open(file, "rb") as f:
            in_patient = False
            arr = []
            while True:
              line = f.readline().decode()
              if not line: break
              line = line.strip()
              if line == "Patient:": 
                in_patient = True
                if arr:
                  l = " ".join(arr)
                  all_lines.append (l)
                  arr = []
                continue
              if line in ("Doctor:", "Description"): 
                in_patient = False
                if arr:
                  l = " ".join(arr)
                  all_lines.append (l)
                  arr = []            
                continue
              if in_patient:
                line = line.replace("  ", " ").replace("  ", " ").strip()
                arr.append(line)
            if arr:
              l = " ".join(arr)
              all_lines.append (l)
              arr = [] 
      all_lines = list(set(all_lines))

      for line in all_lines:
        o.write (line+"\tmedical_dialog\n")
        line = line.replace(" i ", " I ")
        line = line.replace("Hi ","").replace("Hi. ","").replace("Hi, ","").replace("Hello","").replace("hi ","").replace("hi. ","").replace("hi, ","").replace("hello","")
        line_lower = line.lower()
        if "vagina" not in line_lower and "menstra" not in line_lower and "pregna" not in line_lower and "period" not in line_lower and "cervi" not in line_lower and ("son " in line_lower  or "husband" in line_lower or "father" in line_lower or "brother" in line_lower or " male " in line_lower or "testicle" in line_lower or "penis" in line_lower):
          pronoun = "he"
          pronoun2 = "his"
        else:
          pronoun = "she"
          pronoun2 = "her"
        line = line.replace("My son ", "{PERSON}, male ").replace("My daughter ", "{PERSON}, female ").replace("Son ", "{PERSON}, a male ").replace("Daughter ", "{PERSON}, a female ").replace("daughter ", "{PERSON}, a female ").replace(" son ", " {PERSON}, a female ")
        line = line.replace("I'm", f"{pronoun} is").replace("I've", f"{pronoun} has").replace("Am ", "Is ").replace("I have", f"{pronoun} has").replace("I am", f"{pronoun} is").replace("I think", f"{pronoun} thinks").replace("Should I be", f"{pronoun} should be").replace("I ", f"{pronoun} ")
        line = line.replace(" are ", " is ").replace(" us ", " them ").replace(" my ", f" {pronoun2} ").replace(" me ", f" {pronoun2} ").replace("Me ", f"{pronoun2} ")
        line = line.split(".")
        if line:
          line = [l for l in line if l.strip() and not l.endswith("?") and l.lower().split()[0] not in ("what", "where",  "please", "thank")]
        line = ". ".join(line)
        if line:
          line = line.replace("she read that", "are").replace("he read that", "are").replace("Read", "are")
          line = line.replace("My ", "").replace("myself ", "")
          line = line.replace("Should she ", "she should ").replace("Should he ", "he should ")
          if line.startswith("she "):
            line = line.replace("she ", "{PERSON}, a female, ", 1)
          elif line.startswith("he "):
            line = line.replace("he ", "{PERSON}, a male, ", 1)
          line = line.replace("COVID-19", "{DISEASE}").replace("COVID 19", "{DISEASE}").replace("COVID19", "{DISEASE}").replace("COVID", "{DISEASE}")
          line = line.replace("Asian", "{NORP}")
          line = line.replace("France", "{GPE}").replace("Vietnam", "{GPE}").replace("India", "{GPE}").replace("US", "{GPE}")
          o.write (line+"\tmedical_dialog\n")
          

      if not os.path.exists("/content/presidio-research"):
        !git clone https://github.com/microsoft/presidio-research
      import json
      synth_presidio = json.load(open("/content/presidio-research/data/synth_dataset.txt"))
      arr = []
      for s in synth_presidio:
        text = s['full_text']
        #_idx = 0
        ner = [(s['full_text'][s1['start_position']:s1['end_position']], s1['entity_type']) for s1 in s['spans']]
        ner.sort(key=lambda a: len(a), reverse=True)
        for tpl in ner:
          t1, label = tpl
          if t1.strip():
            text = text.replace(t1, "{"+label+"}") #+str(_idx)
            #_idx += 1
        if text:
          o.write (text+"\tpresidio_synth\n")

      sec_contracts = """
EMPLOYMENT AGREEMENT THIS EMPLOYMENT AGREEMENT (the “Agreement”), is made and entered into on this 16th day of September, 2011 (the “Effective Date”), by and between Pharmaceutical Product Development, Inc., a North Carolina corporation (the “Company”), with a mailing address for notice purposes of 929 North Front Street, Wilmington, North Carolina 28401, Attention: Executive Chairman of the Board, and Raymond H. Hill (“Employee”), an individual whose mailing address for notice purposes is 929 North Front Street, Wilmington, North Carolina 28401.
IN WITNESS WHEREOF, the parties hereto have executed this Employment Agreement as of the day and year first above written. COMPANY: PHARMACEUTICAL PRODUCT DEVELOPMENT, INC. By: /s/ Fred N. Eshelman Name: Fred N. Eshelman Title: Executive Chairman EMPLOYEE: /s/ Raymond H. Hill Raymond H. Hill
EMPLOYMENT AGREEMENT. This Employment Agreement (the “Agreement”) is effective as of January 6, 2004
(the “Effective Date”) by and between John O’Keefe (the “Executive”) and Verdisys, Inc., a California corporation (the “Company”). 
IN WITNESS WHEREOF, each of the parties has executed this Agreement, in the case of the
Company by its duly authorized officer, as of the day and year first above written. /s/ John O’Keefe JOHN O’KEEFE VERDISYS, INC By: /s/ Dr. Ron Robinson Name: Dr. Ron Robinson Title: Chairman 
EMPLOYMENT AGREEMENT THIS EMPLOYMENT AGREEMENT (“Agreement”), effective as of September 12, 2011 (the “Effective Date”), is made and entered into by and between The Wendy's Company (the “Company”) and Emil J. Brolick (“Executive”).
All notices and all other communications provided for herein shall be in writing and delivered personally to the other designated party, or mailed by certified or registered mail, return receipt requested, or delivered by a recognized national overnight courier service, as follows: If to the Company to: The Wendy's Company One Dave Thomas Blvd Dublin, Ohio 43017 Attention: General Counsel If to Executive to: (Last address of Executive on the payroll records of the Company unless otherwise directed in writing by Executive) with a copy to: Vedder Price P.C. 222 North LaSalle Street Suite 2600 Chicago, Illinois 60601 Attention: Robert J. Stucker, Esq. Robert F. Simon, Esq.
IN WITNESS WHEREOF, the parties hereto have executed, or caused their duly authorized representatives to execute this Agreement to be effective as of the first date set forth above. “COMPANY” The Wendy's Company By: /s/ Nils H. Okeson_____ Its: Senior Vice President, General Counsel and Secretary “EXECUTIVE” /s/ Emil J. Brolick_________ Emil J. Brolick         
EMPLOYMENT AGREEMENT THIS EMPLOYMENT AGREEMENT (this “Agreement”) is made and entered into this 1st day of May, 2007 by and between Global Payments Inc., a Georgia corporation (the “Company”), and Morgan M. Schuessler, Jr. (“Executive”), to be effective as of the Effective Date, as defined in Section 1.
(f) Notices. All notices, requests, demands and other communications required or permitted hereunder shall be in writing and shall be deemed to have been duly given if delivered or three days after mailing if mailed, first class, certified mail, postage prepaid: To Company: Global Payments Inc. 10 Glenlake Parkway- North Tower Atlanta, Georgia 30328 Office of the Corporate Secretary - 21 - To Executive: Morgan M. Schuessler, Jr. 3889 St. Elisabeth Square Duluth, Georgia 30096
IN WITNESS WHEREOF, the parties hereto have duly executed and delivered this Employment Agreement as of the date first above written. GLOBAL PAYMENTS INC. By: /s/ Suellyn P. Tornay Name: Suellyn P. Tornay Title: General Counsel Date: May 1, 2007 EXECUTIVE: /s/ Morgan M. Schuessler Morgan M. Schuessler, Jr.
EXECUTIVE EMPLOYMENT AGREEMENT This Executive Employment Agreement (the “Agreement”) is made and entered into as of the 15th day of February, 2010, by and between Jeffrey Lang (the “Executive”) and CECO Environmental Corp., a Delaware corporation (the “Company”).
If to the Company: CECO Environmental Corp. 2300 Yonge Street P.O. Box 2408 Toronto, Ontario M4P 1E4 Canada Attention: Phillip DeZwirek If to Executive: To the most recent address of Executive set forth in the personnel records of the Company.
IN WITNESS WHEREOF, the parties hereto have duly executed this Agreement as of the day and year first above written.
CECO ENVIRONMENTAL CORP. EXECUTIVE /s/ Phillip DeZwirek /s/ Jeffrey Lang By: Phillip DeZwirek Jeffrey Lang Title: Chairman	 		 	
EMPLOYMENT AGREEMENT EMPLOYMENT AGREEMENT, dated as of November 2, 2011 (this “Employment Agreement”), by and among Humana Inc., a Delaware corporation (the “Company”), and Bruce Broussard (the “Executive”) (each of the Executive and the Company a “Party,” and together, the “Parties”). 
If to the Company: Humana Inc. 500 West Main Street Louisville, Kentucky Attention: General Counsel Facsimile: 502-508-4073 E-mail Address: ctodoroff@humana.com with a copy to: Fried, Frank, Harris, Shriver & Jacobson LLP One New York Plaza New York, NY 10004 Attention: Donald P. Carleen, Esq. Facsimile: 212-859-4000 E-mail Address: donald.carleen@friedfrank.com If to the Executive: Bruce Broussard at his principal office at the Company (during the Employment Period), and at all times to his principal residence as reflected in the records of the Company.
IN WITNESS WHEREOF, the parties have executed this Employment Agreement as of the date first written above.
HUMANA INC. By: /s/ Bonita Hathcock Name: Bonita Hathcock Title: Senior Vice President and Chief Human Resources Officer EXECUTIVE /s/ Bruce Broussard Bruce Broussard
SERVICES AGREEMENT THIS SERVICES AGREEMENT (the “Agreement”), entered into as of the 20th day of December, 2011 (the “Closing Date”), is by and among MID-CON ENERGY OPERATING, INC., an Oklahoma corporation (the “Services Provider”), MID-CON ENERGY GP, LLC, a Delaware limited liability company (the “General Partner”), MID-CON ENERGY PARTNERS, LP, a Delaware limited partnership (the “MLP”) and MID-CON ENERGY PROPERTIES, LLC, a Delaware limited liability company (the “OLLC”).
If to the Services Provider: Mid-Con Energy Operating, Inc. Attn: Robbin Jones 2431 E. 61st Street, Suite 8500 Tulsa, Oklahoma 74136 Telephone: (918) 743-7575 Fax: (918) 743-8859 If to any member of the MLP Group: c/o Mid-Con Energy GP, LLC Attn: Charles R. Olmstead 2431 E. 61st Street, Suite 850 Tulsa, Oklahoma 74136 Telephone: (918) 743-7575 Fax: (918) 743-8859
IN WITNESS WHEREOF, the Parties have executed this Agreement on, and to be effective as of, the Closing Date. “THE SERVICES PROVIDER” MID-CON ENERGY OPERATING, INC. By: /s/ Charles R. Olmstead Name: Charles R. Olmstead Title: President “GENERAL PARTNER” MID-CON ENERGY GP, LLC By: /s/ Charles R. Olmstead Name: Charles R. Olmstead Title: hief Executive Officer “MLP” MID-CON ENERGY PARTNERS, LP By: MID-CON ENERGY GP, LLC, its general  partner By: /s/ Charles R. Olmstead Name: Charles R. Olmstead Title: Chief Executive Officer “OLLC” MID-CON ENERGY PROPERTIES, LLC By: MID-CON ENERGY PARTNERS, LP, its sole member By: MID-CON ENERGY PARTNERS GP, LLC, its general partner By: /s/ Charles R. Olmstead Name:	 	Charles R. Olmstead Title:	 	Chief Executive Officer
Future Labs V, Inc. – Escrow Services Agreement (December 22nd, 2020)
This Escrow Services Agreement (this “Agreement”) is made and entered into as of by and between Prime Trust, LLC (“Prime Trust” or “Escrow Agent”), _______________________(the “Issuer”) and StartEngine Primary LLC (the “Broker”).
FIRST SUPPLEMENTAL INDENTURE (this “Supplemental Indenture”), dated as of December 21, 2020, among GANNETT CO., INC., a Delaware corporation (the “Company”), the Subsidiary Guarantors party hereto and U.S. BANK NATIONAL ASSOCIATION, a national banking association, as trustee under the indenture referred to below (the “Trustee”).
THIS SEVENTH AMENDMENT TO MEMBERSHIP INTEREST PURCHASE AGREEMENT (this “Amendment”) is entered into effective as of September 22, 2020, by and between DREAM FINDERS HOLDINGS LLC, a Florida limited liability company (“Purchaser”), and H&H CONSTRUCTORS, INC., a North Carolina corporation (“Seller”).
Trust and Servicing Agreement, dated as of November 18, 2020, among Banc of America Merrill Lynch Large Loan, Inc., as Depositor, Wells Fargo Bank, National Association, as Servicer, Situs Holdings, LLC, as Special Servicer, Wilmington Trust, National Association, as Trustee, Wells Fargo Bank, National Association, as Certificate Administrator, as Paying Agent and as Custodian, and Park Bridge Lender Services LLC, as Operating Advisor.
This Securities Purchase Agreement (this “Agreement”), dated as of December 21, 2020, is made by and among TRACON Pharmaceuticals, Inc., a Delaware corporation (the “Company”), and the Purchasers listed on Exhibit A hereto, together with their permitted transferees (each, a “Purchaser” and collectively, the “Purchasers”). The capitalized terms used herein and not otherwise defined have the meanings given them in Article 6.
This FIRST AMENDMENT TO LOAN AND SECURITY AGREEMENT (this “Amendment”) is dated as of March 28, 2019, by and among OUSTER, INC., a Delaware corporation (“Borrower Representative”), and each other Person party hereto as a borrower from time to time (collectively, “Borrowers”, and each, a “Borrower”), the lenders from time to time party hereto (collectively, “Lenders”, and each, a “Lender”), and RUNWAY GROWTH CREDIT FUND INC., as administrative agent and collateral agent for Lenders (in such capacity, “Agent”).
"""
      for line in sec_contracts.split():
        if line:
          o.write (line+"\tsec_contracts\n")

        
  os.system("sort --parallel=32 combined.tsv -o combined.tsv")

  with open("combined_cleaned.tsv", "w", encoding="utf8") as o:
    with open("combined.tsv", "rb") as f:
      prev=""
      while True:
        l = f.readline().decode()
        if not l: break
        l = l.strip()
        l2 = l.replace(":", "").replace("[", "").replace("]", "").replace(".", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace(";", "").replace(" ", "").lower()
        prev2 = prev.replace(":", "").replace("[", "").replace("]", "").replace(".", "").replace("!", "").replace("?", "").replace(",", "").replace("-", "").replace(";", "").replace(" ", "").lower()
        if prev != "" and (l2==prev2 or (len(prev) > 10 and len(l) > 10 and prev2[:10]== l2[:10])):
          if len(l) > len(prev):
            prev = l
          continue
        else:
          if prev:
            if prev[0] < 'וח': 
              o.write (prev.lstrip(':;.+- ')+"\n")
          prev = l
    if prev:
      if prev[0] < 'וח': 
        o.write (prev.lstrip(':;.+- ')+"\n")

  
  os.system("sort --parallel=32 combined_cleaned.tsv -o combined_cleaned.tsv")
  os.system(f"cp combined_cleaned.tsv {share_dir}/combined_cleaned.tsv")
  #os.system("rm ./combined.tsv")
