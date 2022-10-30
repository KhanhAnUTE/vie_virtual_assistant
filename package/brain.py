import pickle
import json
import re
from underthesea import pos_tag
from training.function import fit
from random import randint
from urlextract import URLExtract

with open("asset/data/trained_data.pickle", 'rb') as file:
	vocabs, vectors = pickle.load(file)
with open("asset/data/mind.json", encoding='utf-8') as file:
	data = json.load(file)
with open('asset/data/cities.txt', 'r', encoding='utf-8') as f:
	cities = f.readlines()

my_apps = ['chrome', 'word', 'excel', 'powerpoint', 'calc', 'edge', 'coccoc']

extractor = URLExtract()

def detect_website(you):
	urls = extractor.find_urls(you.lower())
	if urls:
		domain = urls[0]
		tag = 'open website'
		return domain, tag
	else:
		return '', ''
def dectect_application(ans, tag):
	if tag in my_apps:
		ans = tag
		tag = 'open app'
		return ans, tag
	return ans, tag
def detect_keywords_to_search(you, ans, tag):
	pos_tags = pos_tag(you)
	count = 0
	for tup in pos_tags:
		if tup[1] == 'N':
			count += 1
	if count == len(pos_tags):
		ans = you
		tag = 'search google'

	return ans, tag
def detect_city_weather(you, ans, tag):
	if tag == 'weather':
		collection = pos_tag(you.title())
		for item in collection:
			if item[1] == 'Np':
				for city in cities:
					if item[0] in city:
						ans = city
						break
	return ans.strip(), tag

def think(you):
	ans = ""
	tag = ""

	ans, tag = detect_website(you)
	if ans != '':
		return ans, tag

	index = fit(you, vocabs, vectors)
	ans = data["intents"][index]["ans"][randint(0, len(data["intents"][index]["ans"]) - 1)]
	tag = data["intents"][index]["tag"]

	print(tag)

	ans, tag = dectect_application(ans, tag)
	print(tag)
	ans, tag = detect_keywords_to_search(you, ans, tag)
	ans, tag = detect_city_weather(you, ans, tag)

	return ans, tag
