# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import requests
import random
import pickle
import sys
from tqdm import tqdm

def word_addition(A,B):#단어장에 단어와 뜻을 추가합니다. 단어장이 없으면 단어장을 만들어서 단어장을 넣어줍니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('word.txt', 'wb') as f:
			wordlist[A] = B
			pickle.dump(wordlist,f)
	except:
		with open('word.txt','wb') as f:
			pickle.dump({A:B},f)
		
def wordbook(): #단어장을 보여줍니다. 저장해놓은 단어가 없으면 단어장이없다고 메시지가 나옵니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
			for key,val in wordlist.items():
				print("{key} - {value}".format(key=key,value=val))
	except FileNotFoundError:
		print("단어장이 없습니다.")
		
	
def word_test(): #단어테스트를 합니다. 단어가 많으면 10개씩 해서 계속할지 말지 정할 수 있습니다.
	dic = {}
	i = 1
	with open('word.txt', 'rb') as f:
		wordlist = pickle.load(f)
	word = list(wordlist.keys())
	random.shuffle(word)
	for key in word:
		answer = input("{word}: ".format(word=key))
		if(answer != wordlist[key]): 
			print("틀렸습니다.")
			dic[key] = wordlist[key]
		else:
			print("정답입니다")
		i+=1
		if(i%10 == 0):
			a = input("계속하시겠습니까?(y/n) : ")
			if(a == 'y' or a == 'Y'): continue
			else: break
	if(dic != {}): # 오답이 있으면 오답만 출력해줍니다.
		print("\n오답")
		for key,val in dic.items():
			print("{key} - {value}".format(key=key,value=val))
		
def crawling(search): #daum포털사이트 단어사전을 크롤링해서 뜻,예문을 출력해줍니다. 추가 기능도 있습니다.
	dic_url = 'https://dic.daum.net/search.do?q='
	src_url = dic_url + search + '&dic=eng&search_first=Y'
	res = requests.get(src_url)
	html = res.text
	
	soup = bs(html, 'html.parser')
	
	means = soup.select('.cleanword_type.kuek_type > ul > li')

	exm = soup.select('.card_word > .cont_example > ul > li > .box_example.box_sound > .txt_example > .txt_ex')
	
	exm_mean = soup.select('.card_word > .cont_example > ul > li > .box_example.box_sound > .mean_example > .txt_ex')
	
	txt = search.replace('\n','')
	ltxt_mean = []
	if len(means)==1:
		txt_mean = means[0].text
	else:
		for mean in means:
			ltxt_mean.append(mean.text[2:])
		txt_mean = ' '.join(ltxt_mean)

	return txt,txt_mean,'',exm[0].text,exm_mean[0].text
	
def word_search(): #단어검색을 합니다. search변수에 받아서 crawiling함수로 보내줍니다.
	search = input("검색 : ")
	crawling(search)
		
def main(args):       
	ifile = open(args[1], "r")
	ofile = open(args[1]+'.csv', "w")
	ofile.write("단어"+','+"뜻"+','+"발음"+','+"예시"+','+"예시해석"+'\n')
	strings = ifile.readlines()
	for string in tqdm(strings):
		txt,txt_mean,_,exm,exm_mean = crawling(string)
		if txt_mean.replace(" ","")=="":
			print("###############  ", txt+ " was not found")
			continue
		ofile.write(txt+','+txt_mean+','+""+','+exm+','+exm_mean+'\n')
	ifile.close()
	ofile.close()

if __name__ == '__main__':
    main(sys.argv)

