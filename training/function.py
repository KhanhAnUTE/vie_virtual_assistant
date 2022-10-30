import os
import re
import math
import json

re_string = r"\.|,|;|/|:|!|\?|[0-9]"
empty = ""
score_limit = 0.27
score_for_require = 0.1

with open(os.path.dirname(__file__) + '\\..\\asset\\data\\mind.json', encoding='utf-8') as file:
	data = json.load(file)

#read stopword
with open('asset/data/stopwords.txt', 'rt', encoding='utf-8') as file:
    stop_words = file.readlines()
for i in range(len(stop_words)):
    stop_words[i].replace('\n', '')

def clean_data(string):
	#stopwords removal
	for stop_word in stop_words:
		if stop_word in string:
			string = string.replace(stop_word, '')
	#folding case
	string = re.split(re_string, string.lower())
	string = empty.join(string).strip()
	#tokenization
	string = list(dict.fromkeys(string.split()))
	return string

def vectorization(string, vocabs):
	string = clean_data(string)
	vector = [0] * len(vocabs)
	for i in range(len(vocabs)):
		if vocabs[i] in string:
			vector[i] = 1
	return vector
 
def cosine_similar(string, vector, trained_vectors):
	#cos = tích vô hướng / tích độ dài = (x1x2 + y1y2 +...)/(căn(x1^2 + x2^2 +...)căn(x2^2 + y2^2 + ...))
	scores = [] #điểm giữa vector và thành phần trong trained_vector
	for index, trained_vector in enumerate(trained_vectors):
		tich_vo_huong = 0
		do_dai_vector = 0
		do_dai_trained_vector = 0
		for i in range(len(vector)):
			tich_vo_huong += trained_vector[i] * vector[i]
			do_dai_vector += vector[i]**2
			do_dai_trained_vector += trained_vector[i]**2
		if (math.sqrt(do_dai_vector) * math.sqrt(do_dai_trained_vector)) == 0:
			score = 0
		else:
			score = tich_vo_huong/(math.sqrt(do_dai_vector) * math.sqrt(do_dai_trained_vector))
			for require in data['intents'][index]['require']:
				if require in string and require != '':
					score += score_for_require
			if score < score_limit:
				score = 0
		scores.append(score)

	# print(scores)
	if scores.count(0) == len(scores):
		return -1

	return scores.index(max(scores)) #index of maximum scores

def fit(string, vocabs, vectors):
	inp_vector = vectorization(string, vocabs)
	index = cosine_similar(string, inp_vector, vectors)

	return index
