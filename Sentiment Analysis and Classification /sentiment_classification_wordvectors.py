# -*- coding: utf-8 -*-
"""Sentiment_Classification_WordVectors.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ufGD6UmIxNYHkuXHaMmbssMwzIR4DYxc

# Sentiment Analysis with Text Classification

# Importing Libraries
"""

import nltk
import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD

from keras import models
from keras import layers
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

nltk.download('stopwords')
nltk.download('punkt')

"""# Task 1: Extracting Features

## Data Preparation

### Data Preprocessing
"""

amazonReviews = pd.read_csv('amazon_reviews.csv')
amazonReviews = amazonReviews.dropna()
amazonReviews.head(5)

# lowercasing
amazonReviews["reviewText"] = amazonReviews["reviewText"].str.lower()

# removing punctuations
amazonReviews['reviewText'] = amazonReviews['reviewText'].str.translate(str.maketrans(' ', ' ', string.punctuation))

# removing stopwords
stop_words = set(stopwords.words('english'))
amazonReviews['reviewText'] = amazonReviews['reviewText'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# removing numbers
amazonReviews['reviewText'] = amazonReviews['reviewText'].str.replace('\d+', '')

# tokenizing
amazonReviews['reviewText'] = amazonReviews['reviewText'].apply(lambda x: word_tokenize(x))

# changing labels
amazonReviews['overall'] = amazonReviews['overall'].apply(lambda x: 1 if x == 4 or x == 5 else -1)

"""### Data Split"""

# splitting data into training, validation, and test set
features = amazonReviews['reviewText']
target = amazonReviews['overall']
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.1, random_state = 8)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.1, random_state = 8)

"""### Data Statistics"""

# TODO: later
max_length = 0
for review in amazonReviews:
  if len(review) > max_length:
    max_length = len(review)
print("Maximum Length of Sentence: ", max_length)

"""## Representation of Text: word vectors

### Count-based word vectors with co-occurence matrix
"""

def get_vocab(corpus):
    # considering that we are passing the entire dataset i.e. along with the ratings
    vocabulary = [word for review in corpus["reviewText"] for word in review]

    return sorted(set(vocabulary))

def compute_co_occurrence_matrix(corpus, window_size = 4):

    # obtaining the vocabulary
    vocab = get_vocab(corpus)

    # creating word2index
    word2index = {}
    for i in range(len(vocab)):
        word2index[vocab[i]] = i

    # creating M
    M = np.zeros((len(vocab), len(vocab)))
    M = pd.DataFrame(data = M)
    return M, word2index

M, word2index = compute_co_occurrence_matrix(amazonReviews)

M

def reduce_to_k_dim(M, n_components = 2):
    # initializing truncated svd
    svd = TruncatedSVD(n_components = n_components, n_iter = 10)

    # fitting svd on data and transforming the data
    M_reduced = svd.fit_transform(M)

    return M_reduced

M_reduced = reduce_to_k_dim(M)

def plot_embeddings(M_reduced, word2index, words_to_plot):
    for word in words_to_plot:
        idx = word2index[word]
        coordinate = M_reduced[idx]
        plt.scatter(coordinate[0], coordinate[1])

words_to_plot = ['purchase', 'buy', 'work', 'got', 'ordered', 'received', 'product', 'item', 'deal', 'use']
plot_embeddings(M_reduced, word2index, words_to_plot)

"""### Prediction-based word vectors from Glove"""

def load_embedding_model():
    """Load GloVe Vectors
        Return:
            wv_from_bin: All 400000 embeddings, each length 200
    """
    import gensim.downloader as api
    wv_from_bin = api.load("glove-wiki-gigaword-200")

    print("Loaded vocab size %i" % len(list(wv_from_bin.index_to_key)))

    return wv_from_bin

wv_from_bin = load_embedding_model()

def get_matrix_of_vectors(wv_from_bin, required_words):
    import random

    words = list(wv_from_bin.index_to_key)

    print("Shuffling Words")
    random.seed(225)
    random.shuffle(words)
    words = words[:10000]

    print("Putting %i words into word2ind and matrix M..." %(len(words)))
    word2ind = {}
    M = []
    curInd = 0
    for w in words:
        try:
            M.append(wv_from_bin.get_vector(w))
            word2ind[w] = curInd
            curInd += 1
        except KeyError:
            continue

    for w in required_words:
        if w in words:
            continue
        try:
            M.append(wv_from_bin.get_vector(w))
            word2ind[w] = curInd
            curInd += 1
        except KeyError:
            continue

    M = np.stack(M)
    print("Done")

    return M, word2ind

vocab = get_vocab(amazonReviews)
M_glove, word2index_glove = get_matrix_of_vectors(wv_from_bin, vocab)

M_glove_reduced = reduce_to_k_dim(M_glove, n_components = 2)

words_to_plot = ['purchase', 'buy', 'work', 'got', 'ordered', 'received', 'product', 'item', 'deal', 'use']
plot_embeddings(M_glove_reduced, word2index_glove, words_to_plot)

"""## Task 2: Sentiment Classification Algorithms

### Review Embeddings
"""

def review_embeddings(corpus, word2index, M, n_components = 2):

  # reducing dimensions of M_glove
  M_reduced = reduce_to_k_dim(M, n_components = 128)
  M_reduced_averaged = np.average(M_reduced, axis = 1)

  # allocating space to construct review embeddings
  review_embeddings = []
  for review in corpus:
    currReview = []
    for token in review:
      try:
        idx = word2index[token]
        currReview.append(M_reduced_averaged[idx])
      except KeyError:
        currReview.append(0)

    review_embeddings.append(currReview)

  # padding the review embeddings to have same length
  review_embeddings_padded = []
  for embedding in review_embeddings:
    embedding = np.array(embedding)
    if embedding.shape[0] < n_components:
      embedding = np.pad(embedding, pad_width = (0, n_components - embedding.shape[0]), mode = 'constant')
    else:
      embedding = embedding[0:n_components]
    review_embeddings_padded.append(embedding)

  review_embeddings_padded = np.stack(review_embeddings_padded)

  return review_embeddings_padded

review_embeds_train = review_embeddings(X_train, word2index, M, 128)

review_embeds_val = review_embeddings(X_val, word2index, M, 128)

review_embeds_test = review_embeddings(X_test, word2index, M, 128)

"""### Models"""

model = models.Sequential()

# Input - Layer
model.add(layers.Dense(256, activation = "relu", input_shape=(128, )))
# Hidden - Layers
model.add(layers.Dense(128, activation = "relu"))
model.add(layers.Dense(64, activation = "relu"))
model.add(layers.Dense(56, activation = "relu"))
# Output- Layer
model.add(layers.Dense(1, activation = "sigmoid"))

model.compile(optimizer = "adam",loss = "binary_crossentropy",metrics = ["accuracy"])

results = model.fit(review_embeds_train, y_train, epochs= 100, batch_size = 32, validation_data = (review_embeds_val, y_val))

"""### Logistic Regression"""

logistic_regression = LogisticRegression(max_iter = 1000)
logistic_regression.fit(review_embeds_train, y_train)

y_pred = logistic_regression.predict(review_embeds_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)

precision = precision_score(y_test, y_pred)
print("Precision: ", precision)

recall = recall_score(y_test, y_pred)
print("Recall: ", recall)

f1 = f1_score(y_test, y_pred)
print("F1: ", f1)

roc_auc = roc_auc_score(y_test, y_pred)
print("ROC AUC: ", roc_auc)