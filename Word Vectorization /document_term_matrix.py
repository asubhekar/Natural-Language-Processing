# -*- coding: utf-8 -*-
"""Document_Term_Matrix.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y16pIDhk6bjqszbd0KAfhPed8x1t8An2

# <center>Document Term Matrix</center>

<div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. </div>

**Instructions**:
- Please read the problem description carefully
- Make sure to complete all requirements (shown as bullets) . In general, it would be much easier if you complete the requirements in the order as shown in the problem description
- Follow the Submission Instruction to submit your assignment

**Problem Description**

In this assignment, you'll write a class and functions to analyze an article to find out the word distributions and key concepts.

The packages you'll need for this assignment include numpy and pandas. Some useful functions:
- string: `split`,`strip`, `count`,`index`
- numpy: `argsort`,`argmax`, `sum`, `where`

## Define a function to analyze word counts in an input sentence


Define a function named `tokenize(text)` which does the following:
* accepts a sentence (i.e., `text` parameter) as an input
* splits the sentence into a list of tokens by **space** (including tab, and new line).
    - e.g., `it's a hello world!!!` will be split into tokens `["it's", "a","hello","world!!!"]`  
* removes the **leading/trailing punctuations or spaces** of each token, if any
    - e.g., `world!!! -> world`, while `it's` does not change
    - hint, you can import module *string*, use `string.punctuation` to get a list of punctuations (say `puncts`), and then use function `strip(puncts)` to remove leading or trailing punctuations in each token
* only keeps tokens with 2 or more characters, i.e. `len(token)>1`
* converts all tokens into lower case
* find the count of each unique token and save the counts as dictionary, i.e., `{world: 1, a: 1, ...}`
* returns the dictionary
"""

import string
import pandas as pd
import numpy as np
import re

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

def tokenize(text):
    '''
    tokenize(text) accepts a sentence (i.e., text parameter) as an input
    '''

    # splits the sentence into a list of tokens by space (including tab, new line)
    split_text = re.split(r' |\n', text)

    token_new_list = []

    # removes the leading/trailing punctuations or spaces of each token, if any
    puncts = string.punctuation
    for token in split_text:
        if token != '':
            token_new = token.strip(puncts)
            token_new_list.append(token_new.lower())

    vocab = {token: token_new_list.count(token) for token in token_new_list if len(token) > 1}

    return vocab

# test your code
text = """it's a Hello world!!!
           it is hello world again."""
tokenize(text)

"""## Generate a document term matrix (DTM) as a numpy array


Define a function `get_dtm(sents)` as follows:
- accepts a list of sentences, i.e., `sents`, as an input
- uses `tokenize` function you defined in Q1 to get the count dictionary for each sentence
- pools the words from all the strings togehter to get a list of  unique words, denoted as `unique_words`
- creates a numpy array, say `dtm` with a shape (# of docs x # of unique words), and set the initial values to 0.
- fills cell `dtm[i,j]` with the count of the `j`th word in the `i`th sentence
- returns `dtm` and `unique_words`
"""

def get_dtm(sents):

    dtm, all_words = None, []
    #unique_words = []

    for sentence in sents:
        sentence_tokenize = tokenize(sentence)
        for key in sentence_tokenize:
            if key not in all_words:
                all_words.append(key)

    dtm = np.zeros((len(sents), len(all_words)), dtype = np.int8)
    unique_words = all_words

    for i in range(len(sents)):
        tokenized_sent = tokenize(sents[i])
        #tokenized_sent_list = list(tokenized_sent)
        for j in range(len(all_words)):
            if all_words[j] not in tokenized_sent:
                dtm[i, j] = 0
            else:
                dtm[i, j] = tokenized_sent[all_words[j]]



    return dtm, all_words

# A test document. This document can be found at https://hbr.org/2022/04/the-power-of-natural-language-processing

sents = pd.read_csv("sents.csv")
sents.head()
sents.shape
sents.text[0].count("The")

dtm, all_words = get_dtm(sents.text)

# Check if the array is correct

# randomly check one sentence
idx = 3

print(dtm.shape[0],dtm.shape[1])
# get the dictionary using the function in Q1
vocab = tokenize(sents["text"].loc[idx])
print(sorted(vocab.items(), key = lambda item: item[0]))

# get all non-zero entries in dtm[idx] and create a dictionary
# these two dictionaries should be the same
sents.loc[idx]
vocab1 ={all_words[j]: dtm[idx][j] for j in np.where(dtm[idx]>0)[0]}
print(sorted(vocab1.items(), key = lambda item: item[0]))

#print(dtm)

"""## Analyze DTM Array


**Don't use any loop in this task**. You should use array operations to take the advantage of high performance computing.

Define a function named `analyze_dtm(dtm, words, sents)` which:
* takes an array $dtm$ and $words$ as an input, where $dtm$ is the array you get in Q2 with a shape $(m \times n)$, $words$ contains an array of words corresponding to the columns of $dtm$, and $sents$ are the list of sentences you used in Q2.
* calculates the sentence frequency for each word, say $j$, e.g. how many sentences contain word $j$. Save the result to array $df$ ($df$ has shape of $(n,)$ or $(1, n)$).
* normalizes the word count per sentence: divides word count, i.e., $dtm_{i,j}$, by the total number of words in sentence $i$. Save the result as an array named $tf$ ($tf$ has shape of $(m,n)$).
* for each $dtm_{i,j}$, calculates $tf\_idf_{i,j} = \frac{tf_{i, j}}{df_j}$, i.e., divide each normalized word count by the sentence frequency of the word. The reason is, if a word appears in most sentences, it does not have the discriminative power and often is called a `stop` word. The inverse of $df$ can downgrade the weight of such words. $tf\_idf$ has shape of $(m,n)$
* prints out the following:
    
    - the total number of words in the document represented by $dtm$
    - the most frequent top 10 words in this document    
    - words with the top 10 largest $df$ values (show words and their $df$ values)
    - the longest sentence (i.e., the one with the most words)
    - top-10 words with the largest $tf\_idf$ values in the longest sentence (show words and values)
* returns the $tf\_idf$ array.



Note, for all the steps, **do not use any loop**. Just use array functions and broadcasting for high performance computation.
"""

def analyze_dtm(dtm, words, sents):

    dtm, words = get_dtm(sents)
    #words = sorted(words)

    # calculates the sentence frequency for each word
    df = np.zeros((1, dtm.shape[1]))
    df = np.count_nonzero(dtm, axis = 0)

    # normalizes the word count per sentence: divides word count by the total number of words in the sentence
    tf = np.ndarray((dtm.shape[0], dtm.shape[1]))
    tf = dtm / np.sum(dtm, axis = 1)[:, None]

    # for each dtm_i,j calculate tf_idf = tf / df
    tfidf = tf / df

    # print out the following
    print("Total number of words: ", sum(np.sum(dtm, axis = 0)))

    # the most frequent top 10 words in this document
    most_frequent_words = np.sum(dtm, axis = 0)
    most_freq_dictionary = dict(zip(words, most_frequent_words))
    top_10_words = sorted(most_freq_dictionary.items(), key=lambda item: (item[1]), reverse = True)[0:10]
    print("\nMost frequent top 10 words: ", top_10_words)

    # words with the top 10 largest df values
    df_dictionary = dict(zip(words, df))
    top_10_df = sorted(df_dictionary.items(), key = lambda item: item[1], reverse = True)[0:10]
    print("\nTop 10 largest df values: ", top_10_df)

    # the longest sentence
    sentences_length = np.sum(dtm, axis = 1)
    longest_sent_index = np.argmax(sentences_length)
    print("\nThe longest sentence: ", sents[longest_sent_index])


    # top 10 words with the largest tf_idf values in the longest sentence
    longest_sent_tfidf = tfidf[longest_sent_index, :]
    longest_sent_tfidf_dict = dict(zip(words, longest_sent_tfidf))
    top10_longsent_tfidf = sorted(longest_sent_tfidf_dict.items(), key = lambda item: item[1], reverse = True)[0:10]
    #top_10_longsent_tfidf = sorted(top10_longsent_tfidf.keys())
    print("\nTop 10 words with the largest tf_idf values in the longest sentence: ", top10_longsent_tfidf)

    return tfidf

# convert the list to array so you can leverage array operations
words = np.array(all_words)

analyze_dtm(dtm, words, sents.text)

"""## Find keywords of the document (Bonus)

Can you leverage $dtm$ array you generated to find a few keywords that can be used to tag this document? e.g., AI, language models, tools, etc.


Use a pdf file to describe your ideas and also implement your ideas.

## Put everything together and test using main block
"""

# best practice to test your class
# if your script is exported as a module,
# the following part is ignored
# this is equivalent to main() in Java

if __name__ == "__main__":

    # Test Question 1
    text = """it's a hello world!!!
           it is hello world again."""
    print("Test Question 1")
    print(tokenize(text))


    # Test Question 2
    print("\nTest Question 2")
    sents = pd.read_csv("sents.csv")

    dtm, all_words = get_dtm(sents.text)
    print(dtm.shape)


    #3 Test Question 3
    print("\nTest Question 3")
    words = np.array(all_words)

    tfidf= analyze_dtm(dtm, words, sents.text)


