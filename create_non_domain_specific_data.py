#Create synethic PII dataset that is not domain specific
from datasets import load_dataset
import os
import re
import itertools
from re import finditer
import glob
import random

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
  Creates a combined English dataset of non-domain speific PII data. 
  Do some deduplication and cleanup. 
  Add some PII as augumentation (TBD: some <PERSON> and <ORG> tags added. Need to add some more categories).

  See specific licenses for each dataset. We can probably license the whole thing CC non-commercial?
  """    
  

  prev={}
  if not os.path.exists("cleaned_combined.tsv"):
    with open("combined.tsv", "w", encoding="utf8") as o:

      #https://huggingface.co/datasets/newspop#licensing-information - CC-BY
      #download using datasets and use
      dataset = load_dataset("newspop")
      topics_to_ner = {'economy':None, 'microsoft': '<ORG>', 'obama': '<PUBLIC_FIGURE>', 'palestine': '<GPE>'}
      for d in (dataset['train'], ):
        for idx, data in enumerate(d):
          l2, headline, topic = data['title'], data['headline'], data['topic']
          ner_label = topics_to_ner.get(topic)

      """
     @article{Moniz2018MultiSourceSF,
  title={Multi-Source Social Feedback of Online News Feeds},
  author={N. Moniz and L. Torgo},
  journal={ArXiv},
  year={2018},
  volume={abs/1801.07055}
    }   
      """
              
   
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
            l2 = l2.replace("bank account", "<FINANCIAL_PRODUCT> account").replace("card", "<FINANCIAL_PRODUCT>").replace("Google Pay", "<ORG> <FINANCIAL_PRODUCT>").replace("Apple pay", "<ORG> <FINANCIAL_PRODUCT>").replace("American Express", "<FINANCIAL_PRODUCT>")
            l2 = l2.replace("Apple Watch", "<DEVICE>")
            l2 = l2.replace("US", "<GPE>").replace("EU", "<GPE>").replace("UK", "<GPE>").replace("European Union", "<GPE>").replace("Europe", "<GPE>")
            if l2.startswith("Why"): continue
            if (" id " in l2 or "ident" in l2):
              o.write (l2+random.choice([" My id is <GOVT_ID>.", " SSN: <GOVT_ID>.", " My number is <GOVT_ID>."])+"\tbanking77\n")
            elif "get " in l2 or "order " in l2 or "like " in l2 or "want " in l2:
              if random.choice([0,1]):
                o.write (random.choice(["My name is <PERSON>, DOB: <DATE>. ", "<PERSON> here. ", "I'm <PERSON>. "])+ l2+"\tbanking77\n")
              else:
                o.write (l2.strip(' ?.') + random.choice(["? My name is <PERSON>.", "? <PERSON> here.", "? I'm <PERSON>."])+"\tbanking77\n")
            else:
              o.write (l2.strip(' ?.') + random.choice(["? My name is <PERSON>, DOB: <DATE>, Acct #: <CARDINAL>.", "? Asking for acct #: <CARDINAL>.", "? My name is <PERSON>, DOB: <DATE>, Acct #: <CARDINAL>."])+"\tbanking77\n")


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
          l2 = l2.replace("Trump","<PUBLIC_FIGURE_OPINION>").replace("Trump","<PUBLIC_FIGURE_OPINION>").replace("Obama","<PUBLIC_FIGURE_OPINION>").replace("Clinton","<PUBLIC_FIGURE_OPINION>").replace("Trudeau","<PUBLIC_FIGURE_OPINION>")
          l2 = l2.replace('Alaskans', '<NATIONALITY>').replace('Alaskan', '<NATIONALITY>').replace('Alaska', '<GPE>').replace('Americans', '<NATIONALITY>').replace('American', '<NATIONALITY>').replace('America', '<GPE>').replace('Oregon', '<GPE>').replace('United States', '<GPE>').replace('Seattle','GPE')
          l2 = l2.replace("\n", " ").replace("  ", " ").replace("  ", " ")
          l2Arr = l2.split()
          has_a_name = has_any(first_names, l2Arr)
          l2_lower = l2.lower()
          if random.choice([0,1]) and not has_a_name and "mr." not in l2_lower and "ms." not in l2_lower and  "mrs." not in l2_lower and "president" not in l2_lower and "governor" not in l2_lower and  "mayor" not in l2_lower:
            continue
          l2 = " ".join(["<DOMAIN_NAME>" if a.startswith("http") or a.startswith("www") else a for a in l2Arr])
          if len(l2Arr) > 10 and len(l2Arr) < 50 and (score <= 0.5 or random.randint(0, 10)==0): # having too much toxic content may skew the data
            if has_a_name or "mr." in l2_lower or "ms." in l2_lower or "mrs." in l2_lower or "president" in l2_lower or "governor" in l2_lower or "mayor" in l2_lower:
              o.write (l2+"\tcivil_comments\n")
            elif "you " in l2_lower and random.choice([0,1]):
              if l2.startswith("you"):
                l2 = l2.replace("you ", "<PERSON> you ", 1)
                o.write (l2+"\tcivil_comments\n")
              elif l2.startswith("You"):
                l2 = l2.replace("You ", "<PERSON> you ", 1)
                o.write (l2+"\tcivil_comments\n")

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

#create_cleaned_combined()
    
