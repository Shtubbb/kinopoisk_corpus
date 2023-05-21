import json
import random

class Processor:
    def __init__(self, reviews, word2sent, sent_cnt=5, need_dep=False) -> None:
        self.reviews = reviews 
        self.word2sent = word2sent
        self.sent_cnt = sent_cnt
        self.need_dep = need_dep

    def _printDep(self, sentence):
        id = "id"
        head = "head"
        wrd = "word"
        deprel = "deprel"
        pos = "pos"
        return "\n".join([f'id: {word[id]} \t word: {word[wrd]} \tpos: {word[pos]} \thead id: {word[head]} \thead: {sentence[word[head] - 1][wrd] if word[head] > 0 else "root"} \tdeprel: {word[deprel]}' for word in sentence])


    def view(self, word):
        response = f"Ищем слово \"{word}\":\n"
        try:
            sentences = self.word2sent[word]
        except:
            print("К сожалению, такого слова нет:((\n\n")
            return
        cnt = len(sentences)
        response += f"Количество употреблений: {cnt}\n\n"
        for rev_id, sen_id, pos_id in random.sample(sentences, min(self.sent_cnt, cnt)):
            review = self.reviews[rev_id]
            sentence = review["sentences"][sen_id]
            token = sentence["tokens"][pos_id - 1]

            film = review["film"]
            pos = token["pos"]
            word = token["word"]
            feats = token["feats"]
            response += f"Фильм: {film}\n"
            response += f"Часть речи: {pos}\n"
            response += f"Слово: {word}\n"
            response += f"Морфологические свойства: {feats}\n"
            
            response +=  "\n" + sentence["orig"] + "\n\n"

            if self.need_dep:
                response += "Зависимости:\n\n"
                response += self._printDep(sentence["tokens"]) + "\n\n"

            response += "<=======================================================================>\n\n"

        print(response, "\n")


with open('data/corpus.json', 'r') as file:
    reviews = json.JSONDecoder().decode(file.read())

with open('data/index.json', 'r') as file:
    word2sent = json.JSONDecoder().decode(file.read())

need_dep = False
sent_cnt = 1000

processor = Processor(reviews, word2sent, need_dep=need_dep, sent_cnt=sent_cnt)
while True:
    word = input('Введите слово:\n')
    if word == "!!!":
        break
    processor.view(word)

