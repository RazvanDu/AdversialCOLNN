import pickle

dataCONLL = ""
dataONTO = ""

with open('conll.pkl', 'rb') as f:
    dataCONLL = pickle.load(f)

with open('OntoNotes.pkl', 'rb') as f:
    dataONTO = pickle.load(f)

d = {"O": set(), "PERSON": set(), "NORP": set(), "FAC": set(), "ORG": set(), "GPE": set(), "LOC": set(), "PRODUCT": set(), "DATE": set(),
         "TIME": set(), "PERCENT": set(), "MONEY": set(), "QUANTITY": set(), "ORDINAL": set(), "CARDINAL": set(), "EVENT": set(),
         "WORK_OF_ART": set(), "LAW": set(), "LANGUAGE": set()}

def process(tokens, ner_tags, pos_tags, d):
    ln = len(tokens)
    for j in range(ln):
        if ner_tags[j][0] == 'B' and ner_tags[j][1] == '-':

            type = ner_tags[j].replace("B-", "")

            # Remove determiners
            # Check if not in CONLL already by only words in the training test

            #print(tokens[j], " + ", pos_tags[j])

            if pos_tags[j] != 13:
                whole_group = [(tokens[j], pos_tags[j])]
            else:
                whole_group = []

            while j+1 < ln and ner_tags[j+1].startswith("I-"):
                if pos_tags[j+1] != 13:
                    whole_group.append((tokens[j+1], pos_tags[j+1]))
                j += 1

            if len(whole_group) != 0:
                d[type].add(tuple(whole_group))

def process_2(example, i):

    process(example['tokens'], example['ner_tags_str'], example['pos_tags'], d)

    return example

updated_dataset = dataONTO.map(process_2, with_indices=True)

#for key in d.keys():
#    d[key] = list(d[key])

#for dict in numbers:
#    for val in dict.keys():
#        for actual_val in dict[val]:
#            d[val].add(tuple(actual_val))

#print(numbers)

with open('dictionary.pkl', 'wb') as file:
    pickle.dump(d, file)

with open('dictionary.pkl', 'rb') as f:
    d = pickle.load(f)

print("D ", d)

