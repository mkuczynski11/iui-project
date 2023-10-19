import pandas as pd

LABEL_PERCENTAGE = 0.9
def should_be_labeled(word_entry):
    possible_label = word_label(word_entry)
    if (word_entry[possible_label] / word_entry['all'] >= LABEL_PERCENTAGE):
        return True
    return False

def word_label(word_entry):
    most_frequent = 0
    final_label = ''
    for label in word_entry.keys():
        if word_entry[label] > most_frequent and label != 'all':
            most_frequent = word_entry[label]
            final_label = label
    return final_label

df = pd.read_csv('dbdata.csv', encoding='Windows-1252')
print(f'Samples before cleanup: {len(df)}')
df = df[df['sample'].notnull()]
print(f'Samples after removing null sample values: {len(df)}')
words_dict = {}
for _, row_data in df.iterrows():
    text = row_data['sample']
    label = row_data['label']
    for word in text.split(' '):
        if word not in words_dict.keys():
            words_dict[word] = {
                'all': 1,
                label: 1
            }
        else:
            words_dict[word]['all'] = words_dict[word]['all'] + 1
            if label not in words_dict[word].keys():
                words_dict[word][label] = 1
            else:
                words_dict[word][label] = words_dict[word][label] + 1
print(f'Unique words in whole database: {len(words_dict)}')
f = open("stop_words.txt", "r")
for word in f.readlines():
    word = word.strip('\n')
    if word in words_dict.keys():
        words_dict.pop(word)
print(f'Unique words after removing polish stop words: {len(words_dict)}')

labeled_words_dict = {}
for word in words_dict.keys():
    if should_be_labeled(words_dict[word]) and words_dict[word]['all'] > 1:
        labeled_words_dict[word] = word_label(words_dict[word])
print(f'Unique words that fullfill labeled word requirements: {len(labeled_words_dict)}')
for k,v in labeled_words_dict.items():
    print(f'{k}: {v}')