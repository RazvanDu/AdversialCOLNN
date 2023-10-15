import pickle
import datasets
from collections import defaultdict
from numba import jit, cuda

import random

from multiprocessing import Pool

dataCONLL = ""
new_dataset = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('new_dataset.pkl', 'rb') as f:
    new_dataset = pickle.load(f)

index = 15

print(dataCONLL[index]['tokens'])
print(dataCONLL[index]['ner_tags_str'])

print(new_dataset)