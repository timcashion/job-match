
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from job_desc_fxs import return_list, clean_description, remove_escape_chars

#Testing based on sample of data (job_search.job_details_sample)
df = pd.read_csv("bq_sample.csv")
#Focusing on column: 'job_desc'

#return_list function returns the list that follows a certain word. 
#Job description often have list sections (e.g., Requirements: list)
#Defined these manually based on looking through a few postings. 

requirements = ["Qualifications", "Requirements", "Required Skills And Experience", "Background", "background includes",  "Skills", "Needs", "Basic Qualifications", "Must Have"]
responsibilities = ["Responsibilities", "Your Role Is To", "What’s the job?"]
assets = ["Assets", "Additional skills", "Charm Us With", "Preferred Qualifications", "Additional", "Bonus", "we'd love to see you have"]
false_list = [False] * len(requirements)

df["Requirements"] = df["job_desc"].apply(return_list, list_starters=requirements)
df["Responsibilities"] = df["job_desc"].apply(return_list, list_starters=responsibilities)
df["Assets"] = df["job_desc"].apply(return_list, list_starters=assets)

#Check if assets dictionaries are equal to requirement dictionaries
for n in range(1, len(df)):
    if len(df.loc[n, "Requirements"]) > 0:        
        if len(df.loc[n, "Assets"]) > 0:
            for i in range(0, len(df.loc[n, "Requirements"])):
                req_dict = df.loc[n, "Requirements"][i].values()
                for x in range(0, len(df.loc[n, "Assets"])):
                    asset_dict = df.loc[n, "Assets"][x].values()
                    if asset_dict==req_dict:
                        print("Warning: Some 'Asset Lists' are equal to 'Requirement Lists'")

df["Requirements"] = df["Requirements"].astype(str) 
df["Requirements"] = df["Requirements"].str.lower()
df["Assets"] = df["Assets"].astype(str) 
df["Assets"] = df["Assets"].str.lower()
df["Responsibilities"] = df["Responsibilities"].astype(str) 
df["Responsibilities"] = df["Responsibilities"].str.lower()
df["All"] = df["Requirements"].astype(str)  + df["Assets"].astype(str) 
df["All"] = df["All"].str.lower()

#Turn each list into sparse matrices associated with jobs (i.e., BoW cleaning step)
sms_vec = CountVectorizer(min_df=2, tokenizer=nltk.word_tokenize, stop_words='english')
Requirements_counts = sms_vec.fit_transform(df.Requirements)
Assets_counts = sms_vec.fit_transform(df.Assets)
Responsibilities_counts = sms_vec.fit_transform(df.Responsibilities)

#Requirements_counts
