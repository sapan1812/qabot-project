# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import math
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import spacy
from spellchecker import SpellChecker
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import gensim
from gensim import models
from gensim.models import word2vec
from wordcloud import WordCloud
import random

# text cleaning
contractions = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he shall",
    "he'll've": "he shall have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has",
    "i'd": "I would",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": " she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall",
    "what'll've": "what shall have",
    "what're": "what are",
    "what's": "what has",
    "what've": "what have",
    "when's": "when has",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where ha",
    "where've": "where have",
    "who'll": "who shall",
    "who'll've": "who shall have",
    "who's": "who has",
    "who've": "who have",
    "why's": "why has",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you shall",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }
puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
         '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…',
         '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─',
         '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
         '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√']
EMOTICONS = {
        u":‑\)":"Happy face or smiley",
        u":\)":"Happy face or smiley",
        u":-\]":"Happy face or smiley",
        u":\]":"Happy face or smiley",
        u":-3":"Happy face smiley",
        u":3":"Happy face smiley",
        u":->":"Happy face smiley",
        u":>":"Happy face smiley"
    }
chat_words_str = """AFAIK=As Far As I Know
        AFK=Away From Keyboard
        ASAP=As Soon As Possible
        ATK=At The Keyboard
        ATM=At The Moment
        A3=Anytime, Anywhere, Anyplace
        BAK=Back At Keyboard
        BBL=Be Back Later
        BBS=Be Back Soon
        BFN=Bye For Now
        B4N=Bye For Now
        BRB=Be Right Back
        BRT=Be Right There
        BTW=By The Way
        B4=Before
        B4N=Bye For Now
        CU=See You
        CUL8R=See You Later
        CYA=See You
        FAQ=Frequently Asked Questions
        FC=Fingers Crossed
        FWIW=For What It's Worth
        FYI=For Your Information
        GAL=Get A Life
        GG=Good Game
        GN=Good Night
        GMTA=Great Minds Think Alike
        7K=Sick:-D Laugher"""
EMO_UNICODE = {
        u':1st_place_medal:': u'\U0001F947',
        u':2nd_place_medal:': u'\U0001F948',
        u':3rd_place_medal:': u'\U0001F949',
        u':AB_button_(blood_type):': u'\U0001F18E',
        u':ATM_sign:': u'\U0001F3E7',
        u':A_button_(blood_type):': u'\U0001F170',
        u':Afghanistan:': u'\U0001F1E6 \U0001F1EB',
        u':Albania:': u'\U0001F1E6 \U0001F1F1'
    }
UNICODE_EMO = {v: k for k, v in EMO_UNICODE.items()}
chat_words_str = """AFAIK=As Far As I Know
            AFK=Away From Keyboard
            ASAP=As Soon As Possible
            ATK=At The Keyboard
            ATM=At The Moment
            A3=Anytime, Anywhere, Anyplace
            BAK=Back At Keyboard
            BBL=Be Back Later
            BBS=Be Back Soon
            BFN=Bye For Now
            B4N=Bye For Now
            BRB=Be Right Back
            BRT=Be Right There
            BTW=By The Way
            B4=Before
            B4N=Bye For Now
            CU=See You
            CUL8R=See You Later
            CYA=See You
            FAQ=Frequently Asked Questions
            FC=Fingers Crossed
            FWIW=For What It's Worth
            FYI=For Your Information
            GAL=Get A Life
            GG=Good Game
            GN=Good Night
            GMTA=Great Minds Think Alike
            GR8=Great!
            G9=Genius
            IC=I See
            ICQ=I Seek you (also a chat program)
            ILU=ILU: I Love You
            IMHO=In My Honest/Humble Opinion
            IMO=In My Opinion
            IOW=In Other Words
            IRL=In Real Life
            KISS=Keep It Simple, Stupid
            LDR=Long Distance Relationship
            LMAO=Laugh My A.. Off
            LOL=Laughing Out Loud
            LTNS=Long Time No See
            L8R=Later
            MTE=My Thoughts Exactly
            M8=Mate
            NRN=No Reply Necessary
            OIC=Oh I See
            PITA=Pain In The A..
            PRT=Party
            PRW=Parents Are Watching
            ROFL=Rolling On The Floor Laughing
            ROFLOL=Rolling On The Floor Laughing Out Loud
            ROTFLMAO=Rolling On The Floor Laughing My A.. Off
            SK8=Skate
            STATS=Your sex and age
            ASL=Age, Sex, Location
            THX=Thank You
            TTFN=Ta-Ta For Now!
            TTYL=Talk To You Later
            U=You
            U2=You Too
            U4E=Yours For Ever
            WB=Welcome Back
            WTF=What The F...
            WTG=Way To Go!
            WUF=Where Are You From?
            W8=Wait...
            7K=Sick:-D Laugher"""

tags = pd.read_csv('../../Documents/Capstone Project/Dataset/Tags.csv', sep=',')
tags.head()

tags.info()
tags.isna().sum()
tags.fillna('NA', inplace=True)
tags['Tag'] = tags['Tag'].str.lower()
print(tags[tags.Tag == 'python'].shape)

python_tags_df = tags[tags.Tag == 'python']
python_tags_df.sort_values(by='Id')
python_tags_df.head()

print(python_tags_df['Id'].is_unique)

python_questions_df = pd.DataFrame()
chunksize = 10000
i = 0
for chunk in pd.read_csv('../../Documents/Capstone Project/Dataset/Questions.csv', chunksize=chunksize, encoding="ISO-8859-1"):
    if i < 2:
        temp_questions_df = pd.merge(chunk, python_tags_df, on='Id', how='inner')
        python_questions_df = python_questions_df.append(temp_questions_df, ignore_index=True)
    else:
        continue

    i += 1

print(python_questions_df.shape)
print(python_questions_df.head())

python_answers_df = pd.DataFrame()
i = 0
for chunk in pd.read_csv('../../Documents/Capstone Project/Dataset/Answers.csv', chunksize=chunksize, encoding="ISO-8859-1"):
    if i < 4:
        temp_questions_df = pd.merge(chunk, python_tags_df, how='inner', left_on=['ParentId'], right_on=['Id'])
        python_answers_df = python_answers_df.append(temp_questions_df, ignore_index=True)
    else:
        continue

    i += 1

print(python_answers_df.shape)
print(python_answers_df.head())

python_questions_df.drop(['OwnerUserId', 'CreationDate', 'ClosedDate'], axis=1, inplace=True)
python_questions_df.rename(columns={'Body': 'Q_Body', 'Score': 'Q_Score'}, inplace=True)

python_answers_df.drop(['Id_x', 'ParentId',  'CreationDate', 'OwnerUserId', 'Tag'], axis=1, inplace=True)
python_answers_df.rename(columns={'Id_y':'Id', 'Body': 'A_Body', 'Score': 'A_Score'}, inplace=True)

python_merged_df = pd.merge(python_questions_df, python_answers_df, on= 'Id', how='inner')
print(python_merged_df.shape)
print(python_merged_df.head())

python_merged_df.sort_values('Q_Score', ascending=False, inplace=True)
python_merged_df = python_merged_df.reindex(['Id', 'A_Score', 'Q_Score', 'Tag', 'Title', 'Q_Body', 'A_Body'], axis=1)
print(python_merged_df.head())

# Convert to lower case, remove html pattern, url
def convert_to_lower_remove_patterns(text):
    # text = re.sub(r'@[\w]*', '', text)
    text = re.sub(r'<[^<]+?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    text = text.lower()
    return text

# Removal of all characters except of small/ Capital words and numbers
def remove_other_character(text):
    handle_pattern = re.compile(r"[^a-zA-Z0-9 ]")
    return handle_pattern.sub(r'', text)

# Remove short words (length lesser equal to 3)
def remove_small_words(text):
    return ' '.join([w for w in text.split() if len(w) > 3])

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(STOPWORDS, text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

# Removal/Converion of emojis
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def convert_emojis(UNICODE_EMO, text):
    for emot in UNICODE_EMO:
        text = re.sub(r'(' + emot + ')', "_".join(UNICODE_EMO[emot].replace(",", "").replace(":", "").split()), text)
    return text

# Removal of Emoticons
emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS) + u')')
def remove_emoticons(text):
    return emoticon_pattern.sub(r'', text)

# Conversion of emoticons to words
def convert_emoticons(EMOTICONS, text):
    for emot in EMOTICONS:
        text = re.sub(u'(' + emot + ')', "_".join(EMOTICONS[emot].replace(",", "").split()), text)
    return text

# Removal of Frequent Words
def remove_frequent_words(FREQWORDS, text):
    return " ".join([word for word in str(text).split() if word not in FREQWORDS])

# Removal of Rare words
def remove_rare_words(RAREWORDS, text):
    return " ".join([word for word in str(text).split() if word not in RAREWORDS])

# Stemming
def stem_words(text):
    stemmer = PorterStemmer()
    return " ".join([stemmer.stem(word) for word in text.split()])

# Lemmatization
def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

# Remove Chat words
chat_words_map_dict = {}
chat_words_list = []
for line in chat_words_str.split("\n"):
    if line != "":
        cw = line.split("=")[0]
        cw_expanded = line.split("=")[1]
        chat_words_list.append(cw)
        chat_words_map_dict[cw] = cw_expanded
chat_words_list = set(chat_words_list)
def chat_words_conversion(text):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)

cnt = Counter()
python_merged_df['P_Title'] = python_merged_df['Title'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_small_words(text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_Title'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_Title_wo_freq'] = python_merged_df['P_Title'].apply(lambda text:
                                                                        remove_frequent_words(FREQWORDS, text))
python_merged_df['P_Title_wo_freq'] = python_merged_df['P_Title_wo_freq'].apply(lambda text:
                                                                                remove_rare_words(RAREWORDS, text))

print(python_merged_df.head())

python_merged_df['P_Q_Body'] = python_merged_df['Q_Body'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_small_words(text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_Q_Body'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_Q_Body_wo_freq'] = python_merged_df['P_Q_Body'].apply(lambda text:
                                                                          remove_frequent_words(FREQWORDS, text))
python_merged_df['P_Q_Body_wo_freq'] = python_merged_df['P_Q_Body_wo_freq'].apply(lambda text:
                                                                                  remove_rare_words(RAREWORDS, text))

python_merged_df['P_A_Body'] = python_merged_df['A_Body'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_small_words(text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_A_Body'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_A_Body_wo_freq'] = python_merged_df['P_A_Body'].apply(lambda text:
                                                                          remove_frequent_words(FREQWORDS, text))
python_merged_df['P_A_Body_wo_freq'] = python_merged_df['P_A_Body_wo_freq'].apply(lambda text:
                                                                                  remove_rare_words(RAREWORDS, text))

python_merged_df.drop(['P_Title', 'P_Q_Body', 'P_A_Body'], axis=1, inplace=True)
print(python_merged_df.head())

# Most used words using WordCloud
all_title_words = ' '.join([text for text in python_merged_df['P_Title_wo_freq']])
all_body_words = ' '.join([text for text in python_merged_df['P_Q_Body_wo_freq']])
all_combined_words = ' '.join([text for text in python_merged_df['P_A_Body_wo_freq']])

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_title_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_body_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_combined_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

python_merged_df['ProcessedText'] = python_merged_df['P_Title_wo_freq'].str.cat(python_merged_df['P_Q_Body_wo_freq'], sep=" ")
print(python_merged_df.head())
python_merged_df.to_csv('Python_Questions.csv')

# Vectorize the words with best 1000 features for Bag-Of-Words model, TFiDF model and Word2Vec model
# TFiDF
tf_idf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, max_features=1000, stop_words='english')
# tfidf_qstn = tf_idf_vectorizer.fit_transform(python_merged_df['ProcessedText'])
tfidf_answer = tf_idf_vectorizer.fit_transform(python_merged_df['P_A_Body_wo_freq'])
print(tfidf_answer.shape)

# Word2Vec
tokenize_text = python_merged_df['ProcessedText'].apply(lambda x: x.split())
model_w2v = gensim.models.Word2Vec(tokenize_text, size=200, window=5, min_count=2, sg=1, hs=0, negative=10, workers=2, seed=34)
model_w2v.train(tokenize_text, total_examples=len(python_merged_df['ProcessedText']), epochs=20)

tokenize_answer_text = python_merged_df['P_A_Body_wo_freq'].apply(lambda x: x.split())
model_answer_w2v = gensim.models.Word2Vec(tokenize_text, size=200, window=5, min_count=2, sg=1, hs=0, negative=10, workers=2, seed=34)
model_answer_w2v.train(tokenize_answer_text, total_examples=len(python_merged_df['P_A_Body_wo_freq']), epochs=20)

def word_vector(tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0

    for word in tokens:
        try:
            vec += model_w2v[word].reshape((1, size))
            count += 1
        except KeyError:
            continue

    if count != 0:
        vec /= count

    return vec

wordvec_arrays = np.zeros((len(tokenize_text), 200))
for i in range(len(tokenize_text)):
    wordvec_arrays[i,:] = word_vector(tokenize_text[i], 200)
    wordvec_q_df = pd.DataFrame(wordvec_arrays)

print(wordvec_q_df.shape)

wordvec_answer_arrays = np.zeros((len(tokenize_answer_text), 200))
for i in range(len(tokenize_text)):
    wordvec_answer_arrays[i,:] = word_vector(tokenize_answer_text[i], 200)
    wordvec_answer_df = pd.DataFrame(wordvec_answer_arrays)

print(wordvec_answer_df.shape)

model_answer_w2v.wv.save_word2vec_format('model_answer_w2v.bin', binary=True)
print(wordvec_answer_df[0:1])

print(len(pd.unique(python_merged_df['Id'])))

ids = python_merged_df.Id.unique()
random_qstn_id = random.choice(ids)

temp_questions_df = python_merged_df[python_merged_df.Id == random_qstn_id]
temp_answers = python_merged_df[python_merged_df.Id == random_qstn_id][['A_Score', 'P_A_Body_wo_freq']]
temp_answers = temp_answers.sort_values(by='A_Score', ascending=False)

user_input = 'The encoder-decoder model provides a pattern for using recurrent neural networks to address challenging sequence-to-sequence prediction problems, such as machine translation.'
ans = temp_answers['P_A_Body_wo_freq'].tolist()
ans.append(user_input)

tf_idf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, max_features=1000, stop_words='english')
tfs = tf_idf_vectorizer.fit_transform(ans)

pairwise_similarity = tfs * tfs.T
arr = pairwise_similarity.toarray()
np.fill_diagonal(arr, np.nan)
arr

import math
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import spacy
from spellchecker import SpellChecker
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import gensim
from gensim import models
from gensim.models import word2vec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from wordcloud import WordCloud
import random

# text cleaning
contractions = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he shall",
    "he'll've": "he shall have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has",
    "i'd": "I would",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": " she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall",
    "what'll've": "what shall have",
    "what're": "what are",
    "what's": "what has",
    "what've": "what have",
    "when's": "when has",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where ha",
    "where've": "where have",
    "who'll": "who shall",
    "who'll've": "who shall have",
    "who's": "who has",
    "who've": "who have",
    "why's": "why has",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you shall",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }
puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
         '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…',
         '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─',
         '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
         '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√']
EMOTICONS = {
        u":‑\)":"Happy face or smiley",
        u":\)":"Happy face or smiley",
        u":-\]":"Happy face or smiley",
        u":\]":"Happy face or smiley",
        u":-3":"Happy face smiley",
        u":3":"Happy face smiley",
        u":->":"Happy face smiley",
        u":>":"Happy face smiley"
    }
chat_words_str = """AFAIK=As Far As I Know
        AFK=Away From Keyboard
        ASAP=As Soon As Possible
        ATK=At The Keyboard
        ATM=At The Moment
        A3=Anytime, Anywhere, Anyplace
        BAK=Back At Keyboard
        BBL=Be Back Later
        BBS=Be Back Soon
        BFN=Bye For Now
        B4N=Bye For Now
        BRB=Be Right Back
        BRT=Be Right There
        BTW=By The Way
        B4=Before
        B4N=Bye For Now
        CU=See You
        CUL8R=See You Later
        CYA=See You
        FAQ=Frequently Asked Questions
        FC=Fingers Crossed
        FWIW=For What It's Worth
        FYI=For Your Information
        GAL=Get A Life
        GG=Good Game
        GN=Good Night
        GMTA=Great Minds Think Alike
        7K=Sick:-D Laugher"""
EMO_UNICODE = {
        u':1st_place_medal:': u'\U0001F947',
        u':2nd_place_medal:': u'\U0001F948',
        u':3rd_place_medal:': u'\U0001F949',
        u':AB_button_(blood_type):': u'\U0001F18E',
        u':ATM_sign:': u'\U0001F3E7',
        u':A_button_(blood_type):': u'\U0001F170',
        u':Afghanistan:': u'\U0001F1E6 \U0001F1EB',
        u':Albania:': u'\U0001F1E6 \U0001F1F1'
    }
UNICODE_EMO = {v: k for k, v in EMO_UNICODE.items()}
chat_words_str = """AFAIK=As Far As I Know
            AFK=Away From Keyboard
            ASAP=As Soon As Possible
            ATK=At The Keyboard
            ATM=At The Moment
            A3=Anytime, Anywhere, Anyplace
            BAK=Back At Keyboard
            BBL=Be Back Later
            BBS=Be Back Soon
            BFN=Bye For Now
            B4N=Bye For Now
            BRB=Be Right Back
            BRT=Be Right There
            BTW=By The Way
            B4=Before
            B4N=Bye For Now
            CU=See You
            CUL8R=See You Later
            CYA=See You
            FAQ=Frequently Asked Questions
            FC=Fingers Crossed
            FWIW=For What It's Worth
            FYI=For Your Information
            GAL=Get A Life
            GG=Good Game
            GN=Good Night
            GMTA=Great Minds Think Alike
            GR8=Great!
            G9=Genius
            IC=I See
            ICQ=I Seek you (also a chat program)
            ILU=ILU: I Love You
            IMHO=In My Honest/Humble Opinion
            IMO=In My Opinion
            IOW=In Other Words
            IRL=In Real Life
            KISS=Keep It Simple, Stupid
            LDR=Long Distance Relationship
            LMAO=Laugh My A.. Off
            LOL=Laughing Out Loud
            LTNS=Long Time No See
            L8R=Later
            MTE=My Thoughts Exactly
            M8=Mate
            NRN=No Reply Necessary
            OIC=Oh I See
            PITA=Pain In The A..
            PRT=Party
            PRW=Parents Are Watching
            ROFL=Rolling On The Floor Laughing
            ROFLOL=Rolling On The Floor Laughing Out Loud
            ROTFLMAO=Rolling On The Floor Laughing My A.. Off
            SK8=Skate
            STATS=Your sex and age
            ASL=Age, Sex, Location
            THX=Thank You
            TTFN=Ta-Ta For Now!
            TTYL=Talk To You Later
            U=You
            U2=You Too
            U4E=Yours For Ever
            WB=Welcome Back
            WTF=What The F...
            WTG=Way To Go!
            WUF=Where Are You From?
            W8=Wait...
            7K=Sick:-D Laugher"""

tags = pd.read_csv('../../Documents/Capstone Project/Dataset/Tags.csv', sep=',')
tags.head()

tags.info()
tags.isna().sum()
tags.fillna('NA', inplace=True)
tags['Tag'] = tags['Tag'].str.lower()
print(tags[tags.Tag == 'python'].shape)

python_tags_df = tags[tags.Tag == 'python']
python_tags_df.sort_values(by='Id')
python_tags_df.head()

print(python_tags_df['Id'].is_unique)

python_questions_df = pd.DataFrame()
chunksize = 10000
i = 0
for chunk in pd.read_csv('../../Documents/Capstone Project/Dataset/Questions.csv', chunksize=chunksize, encoding="ISO-8859-1"):
    if i < 2:
        temp_questions_df = pd.merge(chunk, python_tags_df, on='Id', how='inner')
        python_questions_df = python_questions_df.append(temp_questions_df, ignore_index=True)
    else:
        continue

    i += 1

print(python_questions_df.shape)
print(python_questions_df.head())

python_answers_df = pd.DataFrame()
i = 0
for chunk in pd.read_csv('../../Documents/Capstone Project/Dataset/Answers.csv', chunksize=chunksize, encoding="ISO-8859-1"):
    if i < 4:
        temp_questions_df = pd.merge(chunk, python_tags_df, how='inner', left_on=['ParentId'], right_on=['Id'])
        python_answers_df = python_answers_df.append(temp_questions_df, ignore_index=True)
    else:
        continue

    i += 1

print(python_answers_df.shape)
print(python_answers_df.head())

python_questions_df.drop(['OwnerUserId', 'CreationDate', 'ClosedDate'], axis=1, inplace=True)
python_questions_df.rename(columns={'Body': 'Q_Body', 'Score': 'Q_Score'}, inplace=True)

python_answers_df.drop(['Id_x', 'ParentId',  'CreationDate', 'OwnerUserId', 'Tag'], axis=1, inplace=True)
python_answers_df.rename(columns={'Id_y':'Id', 'Body': 'A_Body', 'Score': 'A_Score'}, inplace=True)

python_merged_df = pd.merge(python_questions_df, python_answers_df, on= 'Id', how='inner')
print(python_merged_df.shape)
print(python_merged_df.head())

python_merged_df.sort_values('Q_Score', ascending=False, inplace=True)
python_merged_df = python_merged_df.reindex(['Id', 'A_Score', 'Q_Score', 'Tag', 'Title', 'Q_Body', 'A_Body'], axis=1)
print(python_merged_df.head())

# Convert to lower case, remove html pattern, url
def convert_to_lower_remove_patterns(text):
    # text = re.sub(r'@[\w]*', '', text)
    text = re.sub(r'<[^<]+?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    text = text.lower()
    return text

# Removal of all characters except of small/ Capital words and numbers
def remove_other_character(text):
    handle_pattern = re.compile(r"[^a-zA-Z0-9 ]")
    return handle_pattern.sub(r'', text)

# Remove short words (length lesser equal to 3)
def remove_small_words(text):
    return ' '.join([w for w in text.split() if len(w) > 3])

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(STOPWORDS, text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

# Removal/Converion of emojis
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def convert_emojis(UNICODE_EMO, text):
    for emot in UNICODE_EMO:
        text = re.sub(r'(' + emot + ')', "_".join(UNICODE_EMO[emot].replace(",", "").replace(":", "").split()), text)
    return text

# Removal of Emoticons
emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS) + u')')
def remove_emoticons(text):
    return emoticon_pattern.sub(r'', text)

# Conversion of emoticons to words
def convert_emoticons(EMOTICONS, text):
    for emot in EMOTICONS:
        text = re.sub(u'(' + emot + ')', "_".join(EMOTICONS[emot].replace(",", "").split()), text)
    return text

# Removal of Frequent Words
def remove_frequent_words(FREQWORDS, text):
    return " ".join([word for word in str(text).split() if word not in FREQWORDS])

# Removal of Rare words
def remove_rare_words(RAREWORDS, text):
    return " ".join([word for word in str(text).split() if word not in RAREWORDS])

# Stemming
def stem_words(text):
    stemmer = PorterStemmer()
    return " ".join([stemmer.stem(word) for word in text.split()])

# Lemmatization
def lemmatize_words(text):
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

# Remove Chat words
chat_words_map_dict = {}
chat_words_list = []
for line in chat_words_str.split("\n"):
    if line != "":
        cw = line.split("=")[0]
        cw_expanded = line.split("=")[1]
        chat_words_list.append(cw)
        chat_words_map_dict[cw] = cw_expanded
chat_words_list = set(chat_words_list)
def chat_words_conversion(text):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)

cnt = Counter()
python_merged_df['P_Title'] = python_merged_df['Title'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: remove_small_words(text))
python_merged_df['P_Title'] = python_merged_df['P_Title'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_Title'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_Title_wo_freq'] = python_merged_df['P_Title'].apply(lambda text:
                                                                        remove_frequent_words(FREQWORDS, text))
python_merged_df['P_Title_wo_freq'] = python_merged_df['P_Title_wo_freq'].apply(lambda text:
                                                                                remove_rare_words(RAREWORDS, text))

print(python_merged_df.head())

python_merged_df['P_Q_Body'] = python_merged_df['Q_Body'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: remove_small_words(text))
python_merged_df['P_Q_Body'] = python_merged_df['P_Q_Body'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_Q_Body'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_Q_Body_wo_freq'] = python_merged_df['P_Q_Body'].apply(lambda text:
                                                                          remove_frequent_words(FREQWORDS, text))
python_merged_df['P_Q_Body_wo_freq'] = python_merged_df['P_Q_Body_wo_freq'].apply(lambda text:
                                                                                  remove_rare_words(RAREWORDS, text))

python_merged_df['P_A_Body'] = python_merged_df['A_Body'].apply(lambda text: convert_to_lower_remove_patterns(text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_stopwords(STOPWORDS, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: convert_emojis(UNICODE_EMO, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: convert_emoticons(EMOTICONS, text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_other_character(text))
# python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: remove_small_words(text))
python_merged_df['P_A_Body'] = python_merged_df['P_A_Body'].apply(lambda text: stem_words(text))

for text in python_merged_df['P_A_Body'].values:
    for word in text.split():
        cnt[word] += 1

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-10:-1]])

python_merged_df['P_A_Body_wo_freq'] = python_merged_df['P_A_Body'].apply(lambda text:
                                                                          remove_frequent_words(FREQWORDS, text))
python_merged_df['P_A_Body_wo_freq'] = python_merged_df['P_A_Body_wo_freq'].apply(lambda text:
                                                                                  remove_rare_words(RAREWORDS, text))

python_merged_df.drop(['P_Title', 'P_Q_Body', 'P_A_Body'], axis=1, inplace=True)
print(python_merged_df.head())

# Most used words using WordCloud
all_title_words = ' '.join([text for text in python_merged_df['P_Title_wo_freq']])
all_body_words = ' '.join([text for text in python_merged_df['P_Q_Body_wo_freq']])
all_combined_words = ' '.join([text for text in python_merged_df['P_A_Body_wo_freq']])

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_title_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_body_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud_title = WordCloud(width=800, height=500, random_state=21, max_font_size=100).generate(all_combined_words)
plt.rcParams['figure.figsize'] = (14, 8)
plt.imshow(wordcloud_title, interpolation='bilinear')
plt.axis('off')
plt.show()

python_merged_df['ProcessedText'] = python_merged_df['P_Title_wo_freq'].str.cat(python_merged_df['P_Q_Body_wo_freq'], sep=" ")
print(python_merged_df.head())
python_merged_df.to_csv('Python_Questions.csv')

# Vectorize the words with best 1000 features for Bag-Of-Words model, TFiDF model and Word2Vec model
# TFiDF
tf_idf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, max_features=1000, stop_words='english')
# tfidf_qstn = tf_idf_vectorizer.fit_transform(python_merged_df['ProcessedText'])
tfidf_answer = tf_idf_vectorizer.fit_transform(python_merged_df['P_A_Body_wo_freq'])
print(tfidf_answer.shape)

# Word2Vec
tokenize_text = python_merged_df['ProcessedText'].apply(lambda x: x.split())
model_w2v = gensim.models.Word2Vec(tokenize_text, size=200, window=5, min_count=2, sg=1, hs=0, negative=10, workers=2, seed=34)
model_w2v.train(tokenize_text, total_examples=len(python_merged_df['ProcessedText']), epochs=20)

tokenize_answer_text = python_merged_df['P_A_Body_wo_freq'].apply(lambda x: x.split())
model_answer_w2v = gensim.models.Word2Vec(tokenize_text, size=200, window=5, min_count=2, sg=1, hs=0, negative=10, workers=2, seed=34)
model_answer_w2v.train(tokenize_answer_text, total_examples=len(python_merged_df['P_A_Body_wo_freq']), epochs=20)

def word_vector(tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0

    for word in tokens:
        try:
            vec += model_w2v[word].reshape((1, size))
            count += 1
        except KeyError:
            continue

    if count != 0:
        vec /= count

    return vec

wordvec_arrays = np.zeros((len(tokenize_text), 200))
for i in range(len(tokenize_text)):
    wordvec_arrays[i,:] = word_vector(tokenize_text[i], 200)
    wordvec_q_df = pd.DataFrame(wordvec_arrays)

print(wordvec_q_df.shape)

wordvec_answer_arrays = np.zeros((len(tokenize_answer_text), 200))
for i in range(len(tokenize_text)):
    wordvec_answer_arrays[i,:] = word_vector(tokenize_answer_text[i], 200)
    wordvec_answer_df = pd.DataFrame(wordvec_answer_arrays)

print(wordvec_answer_df.shape)

model_answer_w2v.wv.save_word2vec_format('model_answer_w2v.bin', binary=True)
print(wordvec_answer_df[0:1])

print(len(pd.unique(python_merged_df['Id'])))

ids = python_merged_df.Id.unique()
random_qstn_id = random.choice(ids)

temp_questions_df = python_merged_df[python_merged_df.Id == random_qstn_id]
temp_answers = python_merged_df[python_merged_df.Id == random_qstn_id][['A_Score', 'P_A_Body_wo_freq']]
temp_answers = temp_answers.sort_values(by='A_Score', ascending=False)

user_input = 'The encoder-decoder model provides a pattern for using recurrent neural networks to address challenging sequence-to-sequence prediction problems, such as machine translation.'
ans = temp_answers['P_A_Body_wo_freq'].tolist()
ans.append(user_input)

tf_idf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, max_features=1000, stop_words='english')
tfs = tf_idf_vectorizer.fit_transform(ans)

pairwise_similarity = tfs * tfs.T
arr = pairwise_similarity.toarray()
np.fill_diagonal(arr, np.nan)
arr