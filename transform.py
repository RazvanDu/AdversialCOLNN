import pickle
import datasets
from collections import defaultdict

import random

from multiprocessing import Pool

dataCONLL = ""
dataCONLL_train = ""
dataONTO = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('conll_train.pkl', 'rb') as f:
    dataCONLL_train = pickle.load(f)

with open('dictionary.pkl', 'rb') as f:
    loaded = pickle.load(f)

final_tokens = dict()
final_tags = dict()
final_pos = dict()

to_replace = {
    "LOC": list(loaded['GPE']),
    "MISC": list(loaded['PRODUCT'].union(loaded['WORK_OF_ART']).union(loaded['NORP'])),
    "PER": list(loaded['PERSON']),
    "ORG": list(loaded['ORG'])
}

#with Pool(1) as p:
#    numbers = p.map(process_2, range(5, 6))

print(final_tokens)

alread_present = set()

def process_conll_train(example, i):

    tokens = example['tokens']
    ner_tags = example['ner_tags_str']
    pos_tags = example['pos_tags']

    ln = len(tokens)
    for j in range(ln):
        if ner_tags[j][0] == 'B' and ner_tags[j][1] == '-':

            type = ner_tags[j].replace("B-", "")

            # Remove determiners
            # Check if not in CONLL already by only words in the training test

            whole_group = [tokens[j]]

            while j+1 < ln and ner_tags[j+1].startswith("I-"):
                whole_group.append(tokens[j+1])
                j += 1

            alread_present.add(tuple(whole_group))

            #print(whole_group)

def update_dataset(example, i):

    j = 0

    ln = len(example['tokens'])

    result_tokens = []
    result_tags = []
    result_pos = []

    while j < ln:
        # print("J ", j)

        if example['ner_tags_str'][j][0] == 'I' and example['ner_tags_str'][j][1] == '-':
            j = j + 1
            continue

        if example['ner_tags_str'][j][0] == 'B' and example['ner_tags_str'][j][1] == '-':  #

            type = example['ner_tags_str'][j].replace("B-", "")

            temp_j = j

            while temp_j + 1 < len(example['tokens']) and example['ner_tags_str'][temp_j + 1].startswith("I-"):
                temp_j += 1

            temp_j += 1

            while True:

                temp = random.choice(to_replace[type])

                transformed = [tok[0] for tok in temp]

                if tuple(transformed) not in alread_present:
                    break

            replace_tokens = [val[0] for val in temp]
            replace_pos = [val[1] for val in temp]
            replace_tags = [("B-" + type) if i == 0 else ("I-" + type) for i in range(len(temp))]

            result_tokens.extend(replace_tokens)
            result_tags.extend(replace_tags)
            result_pos.extend(replace_pos)

        else:

            result_tokens.append(example['tokens'][j])
            result_tags.append(example['ner_tags_str'][j])
            # print(len(example['tokens']), " + ", len(example['pos_tags']))
            if len(example['pos_tags']) == 0:
                result_pos.append(0)
            else:
                result_pos.append(example['pos_tags'][j])

        j += 1

    example['tokens'] = result_tokens
    example['pos_tags'] = result_pos
    example['ner_tags_str'] = result_tags

    return example

process_train = dataCONLL_train.map(process_conll_train, with_indices=True)

updated_dataset = dataCONLL.map(update_dataset, with_indices=True)

print(to_replace)
print(updated_dataset['tokens'][5])
print(updated_dataset['ner_tags_str'][5])
print(updated_dataset['pos_tags'][5])

with open('new_dataset.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(updated_dataset, file)