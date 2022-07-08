import os, sys
import pandas as pd

from gensim.models import KeyedVectors
from nltk.corpus import stopwords

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(CURRENT_DIR),"hidden"))
sys.path.append(os.path.join(os.path.dirname(CURRENT_DIR),"data"))

from hidden_words import HIDDEN_WORDS

def load_allowed_words(palavras_ptbr):
    """
    Essa função tem por objetivo definir o conjunto de palavras mais comuns da língua portuguesa.
      
    Parameters:
        palavras_ptbr (DataFrame): Conjunto de palavras do idoma português (261798 palavras distintas).
    """

    sw = stopwords.words('portuguese')

    not_allow_list = ['s','am','em','ai','ei','ui','á','í','ando','endo','indo','ondo','ie','amo','emo','armo','aste','ou','inho','inha','ada','ara','sse','eu','ona','rá','i','u','este','esti','era','ava']
    words = []
    for word in palavras_ptbr["Palavras"]:
        if (len(word)>=3) & (word.islower()) & (word.isalpha()):
            check = True
            for not_allow in not_allow_list:
                if word.endswith(not_allow):
                    check=False
            if check and word not in sw:
                words.append(word)
    words = pd.DataFrame(words, columns=["Word"])
    words.to_excel("../data/palavras.xlsx")

def load_file_words(words):
    """
    Essa função tem por objetivo carregar na memória o arquivo contendo a lista de palavras mais similares
    ao conjunto de palavras ocultas.
      
    Parameters:
        words (list): Conjunto de palavras mais comuns do idioma português.
    """
    model = KeyedVectors.load_word2vec_format("../data/skip_s1000.txt", binary=False, encoding="utf8")

    results = pd.DataFrame()
    for i in HIDDEN_WORDS:
        word_dataframe = pd.DataFrame()
        lista = model.most_similar(i,topn=len(model.key_to_index))
        lista.insert(0, (i, 1))
        word_dataframe = pd.DataFrame(lista, columns=["Word", "Similarity"])
        word_dataframe = word_dataframe[word_dataframe['Word'].isin(words["Word"].tolist())].reset_index(drop=True)
        word_dataframe["HIDDEN_WORDS"] = i
        word_dataframe["Position"] = word_dataframe.index+1
        word_dataframe.drop("Similarity", axis=1, inplace=True)
        results = pd.concat([results, word_dataframe])
    
    results.to_excel("../data/results.xlsx")

load_allowed_words(pd.read_csv("../data/palavras_ptbr.txt"))
load_file_words(pd.read_excel("../data/palavras.xlsx"))