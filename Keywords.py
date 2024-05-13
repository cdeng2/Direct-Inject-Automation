# Note: this unverified SSL isn't as secure of a method
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from typing import Callable
import pandas as pd

goodbye_messages = [
    "Sincerely",
    "Yours faithfully",
    "Yours sincerely",
    "Thank you",
    "Best wishes",
    "Cordially",
    "With appreciation",
    "Respectfully yours",
    "Cheers",
    "Thanks",
    "Talk soon",
    "Take care",
    "Regards",
    "All the best"
]

def shorten_email(original:str) -> str:
    """
    Given an unprocessed email from ServiceNow, returns the 
    email body between the greeting and goodbye.

    Catches about 53% of emails (125/232)
    """
    email = original.lower()
    # Assumption: all emails start with "Email Text:"
    displacement: int = 11
    start = email.find('email text:') + displacement
    first_bye: int = -1

    for msg in goodbye_messages:
        i = email.find(msg.lower())
        if first_bye == -1:
            first_bye = i
        elif i != -1 and i < first_bye:
            first_bye = i
    return original[start:first_bye]

def not_stopword(word: str) -> bool:
    """
    Checks if word is NOT a stopword.
    """
    stop_words = set(stopwords.words("english"))
    return word.lower() not in stop_words

def not_digit(word: str) -> bool:
    """
    Checks if word is NOT a digit.
    """
    return not word.isdigit()

def keyword_tags(email: str, conditions: list[Callable[[str], bool]] = 
             [not_stopword, not_digit]) -> list[tuple[str, str]]:
    """
    Given an email body and conditions to determine whether each word 
    is a keyword, returns list of keywords
    """
    words = word_tokenize(email)
    tags = nltk.pos_tag(words)
    filtered: list[str] = []
    for i in range(len(words)):
        iskeyword = True
        for c in conditions:
            if c(words[i]) == False:
                iskeyword = False
                break
        if iskeyword:
            filtered.append(tags[i])
    
    return filtered
    

def get_comment_pos(email:str):
    """
    Returns the short email comment.
    """

    # Tokenize the text into words
    email_body = shorten_email(email)
    ktags = keyword_tags(email_body, conditions = [not_digit])

    comments: list[list[tuple[str,str]]] = []

    find_verb = True
    find_obj = False
    end_chain = False
    for i in range(len(ktags)):
        # print(ktags[i]) if 'VB' in ktags[i][1] else None
        if find_verb and ktags[i][1] == 'VB':
            find_obj = True
            find_verb = False
            temp = [ktags[i]]
        elif find_obj:
            if not end_chain:
                if 'VB' in ktags[i][1] or 'JJ' in ktags[i][1] or 'NN' in ktags[i][1]:
                    temp.append(ktags[i])
                if 'NN' in ktags[i][1]:
                    end_chain = True
            else:
                if 'NN' in ktags[i][1]:
                    temp.append(ktags[i])
                else:
                    find_verb = True
                    find_obj = False
                    end_chain = False
                    comments.append(temp)
    return comments

    # phrase = []
    # for t in range(len(keyword_tags)):
    #     if keyword_tags[t][1] == 'VB':
    #         phrase = [keyword_tags[t]]
    #     adding_nouns = False

    #     if len(phrase) > 0:
    #         if keyword_tags[t][1] != '.':
    #             phrase.append(keyword_tags[t])
    #         else:
    #             comments.append(phrase)
    #             phrase = []
    #             # Phrases may be overwritten
    # return comments

def get_comment_from_pos(email: str):
    tags = get_comment_pos(email)
    message = ''
    for l in tags:
        part = ''
        for tag in l:
            part = part + ' ' + tag[0]
        message = message + part + ' | '
    return message

# with open("temp_text.txt", "r") as file1:
#   text = file1.read().replace("\n", "")
#   (extract_email_body(text))

# df = pd.read_csv('task.csv', encoding='latin-1')
# print(df)

# working with df row 30
# Implement pos tags before removing stopwords next time