
### Dependencies
import pandas as pd
import numpy as np
import re

def clean_description(description_result: str) -> str:
    """
    #Returns cleaned string of description result

    Parameters
    ----------
    description_result: String with HTML formatting contained. 
        Output of return_string function
    Returns
    ----------
    String of description result

    """
    if len(description_result)==0:
        return(None)
    else: 
        description_text = str(description_result)
        description_text = re.sub('<[^<]+?>'," ", description_text)
        description_text = re.sub('  '," ", description_text)
        return(description_text)
assert clean_description("") == None


def remove_escape_chars(text: str) -> str:
    """
    #Returns cleaned string of description result

    Parameters
    ----------
    text: String containing escape characters
    
    Returns
    ----------
    Cleaned string (without escape characters)

    """
    text = text.replace("-", "")
    text = text.replace("[", "")
    text = text.replace("{", "")
    text = text.replace("(", "")
    return(text)
assert remove_escape_chars("-[{(text")=="text"
assert remove_escape_chars("-[[[[[[{(text")=="text"

#return_list function returns the list that follows a certain word. 
#Job description often have list sections (e.g., Requirements: list)
def return_list(text: str, list_starters: list) -> list:
    """
    #Returns list from section that was 'bulleted' in job description based on list_starters

    Parameters
    ----------
    text: String with HTML formatting contained. 
    list_starters: Words to use that often preceed bulleted list in job postings (e.g., "Requirements")
    
    Returns
    ----------
    List of items that followed 'list_starters'. 

    """
    jobs_quals = []
    text = text.lower()
    list_starters = [x.lower() for x in list_starters]
    split_list = text.split("<li>") #Split each list element into its own text.
    text = remove_escape_chars(text)
    text = remove_escape_chars(text)#Need to run twice because of "--"
    false_list = [False] * len(list_starters)
    for i in range(0,len(split_list)):
        text = split_list[i]
        if [x in text for x in list_starters] != false_list:
            y = [x in text for x in list_starters]
            #print(y)
            list_starter = np.array(list_starters)[np.array(y)]
            list_starter = str(list_starter[0])
            
            #Create a list and store each 'qualification' in it
            job_quals = []
            for n in range(i+1, len(split_list)):           
                if "</li>" in split_list[n]:
                    qual = split_list[n]
                    qual = qual.split("</li>")[0]
                    job_quals.append(qual)
                    #print("List item")
            #Define output as a dictionary with the qualification type and the qualifications
            job_dict = {list_starter : job_quals}
            jobs_quals.append(job_dict)
    return(jobs_quals)



