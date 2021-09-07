import requests
import urllib
import csv
from bs4 import BeautifulSoup
# from requests_html import HTML
from requests_html import HTMLSession

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
# headers = {'user_agent': USER_AGENT}

keywords = []
dict_list = []

class googleScrape:
	def __init__(self, dict_list):
		self.dict_list = dict_list
		self.keywords = keywords

	def open_keywords(self):
		with open('keywords.txt', 'r', encoding='utf8') as file:
			self.keywords = file.read().splitlines()
			self.keywords = [k.replace(' ', '+') for k in self.keywords]
			#print(self.keywords)
		return self.keywords

	def get_html(self, link):
		response = HTMLSession().get(link)
		print(response)
		return response

	def make_soup(self, url):
		response = self.get_html(self.URL)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def get_data(self, key, pages):
		for page in range(pages):
			page += 1
			self.URL = f"https://google.com/search?q=site:https://www.searchenginejournal.com/+{key}&start={page}"
			soup = self.make_soup(self.URL)
			links_list = []	
			for div in soup.find_all('div', class_='yuRUbf'):
				link = div.select('a', href=True)
				#print(link[0]['href'])
				links_list.append(link[0]['href'])
			key_dict = {key:links_list}
			dict_list.append(key_dict)
			print(dict_list)
				
			for div in soup.find_all('div', class_='LHJvCe'):
				#print(type(div.text))
				print(f'{key}: {div.text}')

	def main(self):
		self.open_keywords()
		pages = 2
		for key in self.keywords:
			self.get_data(key, pages)

run = googleScrape(dict_list) 

if __name__ == '__main__':
	run.main()
