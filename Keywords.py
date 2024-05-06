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

def keywords(email: str, conditions: list[Callable[[str], bool]] = 
             [not_stopword, not_digit]) -> list[str]:
    """
    Given an email body and conditions to determine whether each word 
    is a keyword, returns list of keywords
    """
    words = word_tokenize(email)
    filtered: list[str] = []
    for word in words:
        iskeyword = True
        for c in conditions:
            if c(word) == False:
                iskeyword = False
                break
        if iskeyword:
            filtered.append(word)
    
    return filtered
    

def get_comment(email:str):
    """
    Returns the short email comment.
    """

    # Tokenize the text into words
    words = word_tokenize(email)
    tags = nltk.pos_tag(words)
    print([tag for tag in tags if 'VB' in tag[1]])

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in words if not word.isdigit() and 
                word.lower() not in stop_words]
    keyword_tags = [tag for tag in tags if tag[0] in keywords]
    print(keyword_tags)

    comments: list[list[tuple[str,str]]] = []

    phrase = []
    for t in range(len(keyword_tags)):
        if keyword_tags[t][1] == 'VB':
            phrase = [keyword_tags[t]]
        adding_nouns = False

        if len(phrase) > 0:
            if keyword_tags[t][1] != '.':
                phrase.append(keyword_tags[t])
            else:
                comments.append(phrase)
                phrase = []
                # Phrases may be overwritten
    return comments

# with open("temp_text.txt", "r") as file1:
#   text = file1.read().replace("\n", "")
#   (extract_email_body(text))

df = pd.read_csv('task.csv', encoding='latin-1')
# print(df)

# working with df row 30
# Implement pos tags before removing stopwords next time