import glob
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk.tokenize import sent_tokenize
import nltk
#nltk.download('punkt')
#apt install libtinfo5
#install torch using anaconda
#from transformers import *
import pandas as pd
from summarizer import Summarizer
def load_Dataset():
    data_list = []
    for filename in glob.glob("/home/jamie/Downloads/case_doc/*.txt"):
        fp = open(filename, 'r')
        content = fp.read()
       # print(content)
        data_list.append((filename, content))
        fp.close()
    return data_list
#dataframe with filename and paragraph
def Data_preparation(data_list):
    data_tags=["filename","content"]
    data1 = pd.DataFrame.from_records(data_list, columns=data_tags)
    return(data1)
#creating a new column summary
def SummarizationBERT(data1):
    for index, row in data1.iterrows():
        #print(row['content'])
        data1.loc[index,"summary"]=""

        #create summarization using BERT
    model = Summarizer()
    for index, row in data1.iterrows():
    # print(row["paragraphs"])
    # data.loc[index,"summarizer"]=" writing sumarizer in some time"
        result = model(row['content'])
        full = ''.join(result)
        data1.loc[index, "title"] = full
    return data1
def write_to_csv():
  # with open('/content/drive/My Drive/legal_cases_summarize.csv', 'w') as f:
    #data1.to_csv(f)
    print("empty")
def read_from_csv():
    data2 = pd.read_csv("/home/jamie/Downloads/legal_cases_summarize.csv", index_col=[0])
    # data2["paragraphs"]=data2["content"]
    data2["summary"] = data2["title"]
    newdata = data2[["filename", "summary", "content"]]
    return(newdata)
def find_chief_justice(content):
    if type(content) !=str:
        return "NULL"
    m = re.search('(?<=HON’BLE)(.*)', content)
    if(m):
        # print("the Chief justice:", m.groups())
         return(m.groups())
    else:
        return "NULL"

def applicant_case(data):

    query = "for the applicant"
    if type(data) != str:
        return "NULL"
    choices = sent_tokenize(data)
    applicant = process.extractOne(query, choices)
    return applicant

def respondent_case(data):
    if type(data) != str:
        return "NULL"
    query = "for the respondent."
    choices = sent_tokenize(data)
    respondent = process.extractOne(query, choices)
    return respondent

def case_about(data):
    query = "IPC section PIL bail Procedure."
    if type(data) != str:
        return "NULL"
    choices = sent_tokenize(data)
    case_about =process.extractOne(query, choices)
    return case_about

if __name__=="__main__":

    data=load_Dataset()
    data1=Data_preparation(data)
   # print(data1)
    newdata = read_from_csv()
    newdata["justice"]= newdata["content"].apply(find_chief_justice)
    newdata["applicant"] = newdata["content"].apply(applicant_case)
    newdata["respondent"] = newdata["content"].apply(applicant_case)
    newdata["case_about"] = newdata["content"].apply(case_about)
   # SummarizationBERT(data1)
    print(newdata.head(20))
    newdata.to_csv("test_dataset.csv")