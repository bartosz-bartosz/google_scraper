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
no_results_list = []

class googleScrape:
	def __init__(self, dict_list, no_results_list):
		self.dict_list = []
		self.keywords = []
		self.no_results_list = []


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

	def no_results_csv(self, no_results_list):
		print('Number of results for all keywords:')
		print(no_results_list)
		no_results_file = 'no_results.csv'
		with open(no_results_file, 'w', newline='') as resultsfile:
			writer = csv.writer(resultsfile)
			for dic in no_results_list:
				writer.writerows(dic.items())


	def get_data(self, key, pages):
		links_list = []
		for page in range(pages):
			page = str(page) + '0'
			self.URL = f"https://google.com/search?q=site:https://www.searchenginejournal.com/+{key}&start={page}"
			print(self.URL)
			soup = self.make_soup(self.URL)
			for div in soup.find_all('div', class_='LHJvCe'):
				#print(type(div.text))
				if int(page) > 0:
					continue
				else:
					no_results = div.text
					self.no_results_list.append({key:no_results})
					print(f'{key}: {no_results}')
					print('\n')
			for div in soup.find_all('div', class_='yuRUbf'):
				link = div.select('a', href=True)
				#print(link[0]['href'])
				links_list.append(link[0]['href'])
				print(links_list)
			# for link in links_list:
			# 	# link_index = str(links_list.index(link)+1)	
			# 	links_list.append(link)
			# 	key_dict = {key:link}
			# 	dict_list.append(key_dict)
					

		key_dict = {key:links_list}
		dict_list.append(key_dict)
		# return self.no_results_csv(self.no_results_list)
		print(dict_list)


	def main(self, pages):
		self.open_keywords()
		for key in self.keywords:
			self.get_data(key, pages)
		self.no_results_csv(self.no_results_list)

run = googleScrape(dict_list, no_results_list) 

if __name__ == '__main__':
	run.main(2)
