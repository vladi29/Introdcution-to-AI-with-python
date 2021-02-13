import nltk
import sys
import os
import string
from math import log
import operator

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for txt in os.listdir(directory):
        with open(os.path.join(directory, txt), "r", encoding="utf8") as f:  #Is necessary utf8 encoding to read the file
            files[txt] = f.read()

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = list()
    document = document.lower()
    toks = nltk.word_tokenize(document)
    for word in toks:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            words.append(word) 
    
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs_dict = dict()
    total_docs = len(documents.keys())

    for doc in documents.keys():
        for word in documents[doc]:
            if word not in idfs_dict:
                idfs_dict[word] = log(total_docs/appear(word, documents))

    return idfs_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    Tfiles = list()
    tf_idf_dict = dict()        #aux dict to save and order the files
    tf_idf_list = list()

    for doc in files.keys():
        tf_idf = 0
        for word in query:
            tf_idf = tf_idf + files[doc].count(word)*idfs[word]   #save tf*idf for each doc in a var to order it in a dict
        tf_idf_dict[doc] = tf_idf
    
    tf_idf_list = sorted(tf_idf_dict.items(), key=operator.itemgetter(1), reverse=True) #ordering the dict 

    for item in tf_idf_list:
        Tfiles.append(item[0])
    
    Tfiles = Tfiles[:n]

    return Tfiles

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    Tsentences = list()
    top_stcs = list()
    for sentence in sentences:
        mwm = 0                                     #matching word measure
        total_words = len(sentences[sentence])      #Total words in a sentece
        qtd = 0                                     #Initial query term density
        for word in query:
            if word in sentences[sentence]:
                mwm = mwm + idfs[word]
                qtd = qtd + sentences[sentence].count(word)/total_words
        Tsentences.append([sentence, mwm, qtd])

    Tsentences = sorted(Tsentences, key=lambda item: (item[1], item[2]), reverse=True)

    for item in Tsentences:
        top_stcs.append(item[0])
    
    top_stcs = top_stcs[:n]

    return top_stcs

def appear(word, documents):
    """
    This function calculate the amount of documents in which a word appears
    """
    times_appear = int()

    for doc in documents:
        if word in documents[doc]:
            times_appear = times_appear + 1
        
    return times_appear

if __name__ == "__main__":
    main()
