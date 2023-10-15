import pickle
import datasets
from collections import defaultdict
from numba import jit, cuda

import random

from multiprocessing import Pool

dataCONLL = ""
dataONTO = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('dictionary.pkl', 'rb') as f:
    loaded = pickle.load(f)

final_tokens = dict()
final_tags = dict()
final_pos = dict()

to_replace = {
    "LOC": list(loaded['FAC'].union(loaded['GPE'])),
    "MISC": list(loaded['PRODUCT'].union(loaded['WORK_OF_ART']).union(loaded['NORP'])),
    "PER": list(loaded['PERSON']),
    "ORG": list(loaded['ORG'])
}

def process_2(i):

    print(i)

    doc_dif = 0

    #tokens = dataCONLL['tokens'][i]
    #pos = dataCONLL['pos_tags'][i]
    #tags = dataCONLL['ner_tags_str'][i]

    j = 0

    ln = len(dataCONLL['tokens'][i])

    result_tokens = []
    result_tags = []
    result_pos = []

    while j < ln:
        #print("J ", j)

        if dataCONLL['ner_tags_str'][i][j][0] == 'I' and dataCONLL['ner_tags_str'][i][j][1] == '-':
            j = j+1
            continue

        if dataCONLL['ner_tags_str'][i][j][0] == 'B' and dataCONLL['ner_tags_str'][i][j][1] == '-':#

            type = dataCONLL['ner_tags_str'][i][j].replace("B-", "")

            temp_j = j

            while temp_j+1 < len(dataCONLL['tokens'][i]) and dataCONLL['ner_tags_str'][i][temp_j+1].startswith("I-"):
                temp_j += 1

            temp_j += 1

            temp = random.choice(to_replace[type])

            replace_tokens = [val[0] for val in temp]
            replace_pos = [val[1] for val in temp]
            replace_tags = [("B-" + type) if i == 0 else ("I-" + type) for i in range(len(temp))]

            result_tokens.extend(replace_tokens)
            result_tags.extend(replace_tags)
            result_pos.extend(replace_pos)

        else:

            result_tokens.append(dataCONLL['tokens'][i][j])
            result_tags.append(dataCONLL['ner_tags_str'][i][j])
            #print(len(dataCONLL['tokens'][i]), " + ", len(dataCONLL['pos_tags'][i]))
            if(len(dataCONLL['pos_tags'][i]) == 0):
                result_pos.append(0)

        #print("J ", result_tokens)

        j += 1

    print("HERE ", final_tokens)

    final_tokens[i] = final_tokens

    print("HERE2 ", final_tokens)

    final_pos[i] = final_pos
    final_tags[i] = final_tags

    #dataCONLL['doc'][i] = ln

    #process(dataONTO['tokens'][i], dataONTO['ner_tags_str'][i], dataONTO['pos_tags'][i], d)

    return i

#with Pool(1) as p:
#    numbers = p.map(process_2, range(5, 6))

print(final_tokens)

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

            while temp_j + 1 < len(example['tokens']) and example['ner_tags_str'][temp_j + 1].startswith(
                    "I-"):
                temp_j += 1

            temp_j += 1

            temp = random.choice(to_replace[type])

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
            if (len(example['pos_tags']) == 0):
                result_pos.append(0)

        # print("J ", result_tokens)

        j += 1

    example['tokens'] = result_tokens
    example['pos_tags'] = result_pos
    example['ner_tags_str'] = result_tags

    return example

updated_dataset = dataCONLL.map(update_dataset, with_indices=True)

print(to_replace)
print(updated_dataset['tokens'][5])
print(updated_dataset['ner_tags_str'][5])
print(updated_dataset['pos_tags'][5])

with open('new_dataset.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(updated_dataset, file)