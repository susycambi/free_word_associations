#!/usr/bin/env python
# coding: utf-8

import io, os, csv, re
import pandas as pd
import numpy as np
# from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx
# from pyvis.network import Network
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk import pos_tag, word_tokenize, punkt
import spacy
import fr_core_news_md
import math
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# from spellchecker import SpellChecker
import statistics
import argparse
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", help="Directory path of the project")
    return parser.parse_args()

# Define functions relevant for the SWOW processing
def load_swow_data(project_dir):
    data = pd.read_csv(os.path.join(project_dir, "ToT_transcripts.csv"))
    data['associations'] = data['word'] + '_' + data['number'].astype(str).str.strip('.0')
    data.drop(data.columns[[1, 14, 15, 16]], axis=1, inplace=True) # added that I drop the "number" column
    return data

nlp = spacy.load('fr_core_news_md')

def preprocess_text(text, nlp):
    # Load the appropriate language model
    
    filler_words = ['un', 'une', 'et', 'le', 'la', 'etc.', 'TRUE', 'FALSE', 'x', '?', 'No more responses', 'Unknown word']
    # Text cleaning
    text = text.lower() # puts everything in lower case
    print("here: pre-tokenization", text)
    text = text.replace("-", " ")  # Replace hyphens with spaces
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])  # Remove non-alphanumeric characters except spaces
    text = text.strip()  # Remove leading/trailing spaces
    # text = ' '.join(word for word in text.split() if len(word.split()) == 1) # joining multiple word responses
    # Remove strings that contain numbers
    text = re.sub(r'\b\w*\d\w*\b', '', text) # shouldn't this be before introducing tokens
    
    # Tokenization
    tokens = text.split()  # Split on whitespace instead of using word_tokenize
    
    # Stopword removal ("le", "mais", "du")
    stop_words = set(stopwords.words('french'))
    
    tokens = [token for token in tokens if token not in stop_words and token not in filler_words]

    # Lemmatization
    
    print("AFTER:", tokens)
  
    doc = nlp(''.join(tokens))
    print("DOC:_____", doc)
    lemmatized_tokens = [token.lemma_ for token in doc]
    
    return lemmatized_tokens

def filter_and_preprocess_swow_data(data):

    # Drop NaNs/missing cues/responses from analysis 
    print(data.head())
    df_clean = data.replace('?', np.nan)
    # df_clean = data.dropna() ##change to drop any NAs in your columns
    print(df_clean.head())
    # df_clean = data.fillna('', inplace=True)

    # Preprocess the data based on the lang argument with spell checking
    df_preprocessed = df_clean.fillna('').applymap(lambda x: preprocess_text(x, nlp)) # = run proprocess_text() on df_preprocessed element-wise

    return df_preprocessed

def save_preprocessed_data(df_preprocessed, project_dir):
    file_name  = "words-n-stuff.csv"
    path_to_file = os.path.join(project_dir, file_name)
    df_preprocessed.to_csv(path_to_file, index=False)
    print("Preprocessed & spell-checked dataset has been saved to:", project_dir)

## Finally, let's run !!
def run_forest_run(project_dir):
   
    data = load_swow_data(project_dir)
    
    # Filter and preprocess the data
    print("Pre-processing the dataset (this can take a while)...")
    df_preprocessed = filter_and_preprocess_swow_data(data)

    # Save the preprocessed data to a CSV file
    save_preprocessed_data(df_preprocessed, project_dir)
    
    print("Preprocessing complete! :D")

if __name__ == '__main__':
    args = parse_arguments()
    project_dir = args.project_dir
    run_forest_run(project_dir)
