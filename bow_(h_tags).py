# -*- coding: utf-8 -*-
"""BoW (h tags).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CpAKRE31R3CDoNhZYQxFvWHEviKwsP7F
"""

!pip3 install newspaper3k

import requests
import re
from newspaper import Article
from bs4 import BeautifulSoup
bag_of_h=[]
def getText(url):
  url_= requests.get(url)
  soup= BeautifulSoup(url_.text, 'html.parser')
  get_h1=[i.get_text() for i in soup.find_all('h1')]
  get_h2=[j.get_text() for j in soup.find_all('h2')]
  get_h3=[k.get_text() for k in soup.find_all('h3')]
  
  for h in get_h1:
    bag_of_h.append(h)
  for j in get_h2:
    bag_of_h.append(j)
  for k in get_h3:
    bag_of_h.append(k)
  print(bag_of_h)

  
getText("http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/")

# import statments
import numpy
import re


def tokenize(sentences):
    words = []
    for sentence in sentences:
        w = word_extraction(sentence)
        words.extend(w)
        
    words = sorted(list(set(words)))
    return words

def word_extraction(sentence):
    ignore = ['a', "the", "is"]
    words = re.sub("[^\w]", " ",  sentence).split()
    cleaned_text = [w.lower() for w in words if w not in ignore]
    return cleaned_text    
    
def generate_bow(allsentences):    
    vocab = tokenize(allsentences)
    print("Word List for Document \n{0} \n".format(vocab));

    for sentence in allsentences:
        words = word_extraction(sentence)
        bag_vector = numpy.zeros(len(vocab))
        for w in words:
            for i,word in enumerate(vocab):
                if word == w: 
                    bag_vector[i] += 1
                    
        print("{0} \n{1}\n".format(sentence,numpy.array(bag_vector)))
allsentences=bag_of_h
generate_bow(allsentences)
