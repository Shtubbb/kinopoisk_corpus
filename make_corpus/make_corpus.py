import stanza
import json
import string 
from collections import defaultdict
from tqdm import tqdm

def prettify(text):
    res = ''
    before_point = True
    for i in range(len(text)):
        char = text[i]
        if text[i] in string.ascii_lowercase:
            char = text[i]
            if before_point:
                before_point = False
                char = char.upper()
        elif text[i] in  string.punctuation:
            res = res[:-1] ##remove space
            if text[i] == '.':
                before_point = True
        res += char
    
    return res

def process_reviews(reviews):
    word2sentence = defaultdict(list)
    pipeline = stanza.Pipeline('ru', processors='tokenize,pos,lemma,depparse')
    for rev_id, review in tqdm(enumerate(reviews)):
        doc = pipeline(review['content'])
        sentences = []
        for sen_id, dsentence in enumerate(doc.sentences):
            original_sentence = ''
            sentence = dict()
            sentence['tokens'] = []
            original_sentence = []
            for word in dsentence.words:
                original_sentence.append(word.text)
                token = dict()
                token['word'] = word.text
                token['lemma'] = word.lemma
                token['pos'] = word.upos
                token['id'] = word.id
                token['head'] = word.head
                token['deprel'] = word.deprel
                token['feats'] = word.feats
                word2sentence[word.lemma].append((rev_id, sen_id, word.id))
                sentence['tokens'].append(token)
            sentence['orig'] = prettify(' '.join(original_sentence))
            sentences.append(sentence)
        review['sentences'] = sentences
        del review['content']
    return reviews, word2sentence

with open('reviews.json', 'r') as file:
    reviews = json.JSONDecoder().decode(file.read())

reviews, word2sentence = process_reviews(reviews)

with open("../data/corpus.json", 'w+') as file:
    json.dump(reviews, file)

with open("../data/index.json", 'w+') as file:
    json.dump(word2sentence, file)
