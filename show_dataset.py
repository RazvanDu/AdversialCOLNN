import pickle
import datasets
from collections import defaultdict

import random

from multiprocessing import Pool

dataCONLL = ""
new_dataset = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('new_dataset.pkl', 'rb') as f:
    new_dataset = pickle.load(f)

index = 17

print(dataCONLL[index]['tokens'])
print(dataCONLL[index]['ner_tags_str'])
print(dataCONLL[index]['pos_tags'])

print(new_dataset[index]['tokens'])
print(new_dataset[index]['ner_tags_str'])
print(new_dataset[index]['pos_tags'])