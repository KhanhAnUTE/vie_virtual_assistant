'''Đây là file dùng để đào tạo model'''
import os
import pickle
from training.function import clean_data, vectorization, data
from training.import_data import *

#list chứa các câu hỏi của mỗi chủ đề
#vd lst = ["xin chào chào bạn", "bạn có khỏe không sức khỏe sao rồi"]
documents = []
space_string = ' '
for intent in data['intents']:
	documents.append(space_string.join(intent['ques']))
# print(documents)
#tạo từ vựng
vocabs = space_string.join(documents)
vocabs = clean_data(vocabs)

print('Successful create vocabularies')

#tạo vector
vectors = []
for document in documents:
	vector = vectorization(document, vocabs)
	vectors.append(vector)

print('Successful create vectors')

#Sau khi train xong thì lưu kq train lại để cho ngta dùng
filename = os.path.dirname(__file__) + '/asset/data/trained_data.pickle'
# Its important to use binary mode
with open(filename, 'wb') as file:
	pickle.dump((vocabs, vectors), file)

print("Successful build model")