import requests
import urllib
import re
import csv
import time
import unicodedata
from bs4 import BeautifulSoup
from requests_html import HTMLSession

keywords = []
dict_list = []
no_results_list = []
pages_to_scrape = 5
delay = 0

class googleScrape:
	def __init__(self, dict_list, no_results_list):
		self.dict_list = []
		self.keywords = []
		self.no_results_list = []

	def open_keywords(self):
		with open('keywords.txt', 'r', encoding='utf8') as file:
			self.keywords = file.read().splitlines()
			self.keywords = [k.replace(' ', '+') for k in self.keywords]
		return self.keywords

	def get_html(self, link):
		response = HTMLSession().get(link)
		print(response)
		if response.status_code == 200:
			print('Response OK, data reached successfully.\n')
			return response
		else:
			print("\nToo many tries. Saving data collected until now.\nTry again in a few minutes.If problem persists, set higher delay.\n")
			if len(self.no_results_list) < 1:
				print('\nNo data to save.')
				exit()
			else:
				self.no_results_csv(self.no_results_list)
				self.links_csv(self.dict_list)
				exit()
 
	def make_soup(self, url):
		response = self.get_html(self.URL)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def no_results_csv(self, no_results_list):
		print('\n')
		print(type(no_results_list[0]))
		no_results_file = 'no_results.csv'
		with open(no_results_file, 'w', newline='') as resultsfile:
			writer = csv.DictWriter(resultsfile, no_results_list[0].keys())
			writer.writeheader()
			writer.writerows(no_results_list)

		print(f'Number of results for each keyword saved to {no_results_file}')

	def links_csv(self, dict_list):
		csv_file ='output_links.csv'
		headers = ['keyword','link']
		with open(csv_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(headers)
			for dic in dict_list:
				for key, items in dic.items():
					for item in items:
						writer.writerow([key, item])
		print(f'Links saved to {csv_file}')

	def get_data(self, key, pages, delay):
		links_list = []
		print('\n')
		print(f'Getting data for keyword >>{key.upper()}<<')
		for page in range(pages):
			page = str(page) + '0'
			self.URL = f"https://google.com/search?q=site:https://www.searchenginejournal.com/+{key}&start={page}"
			print(self.URL)
			soup = self.make_soup(self.URL)
			for div in soup.find_all('div', class_='LHJvCe'):
				if int(page) > 0:
					continue
				else:
					no_results = div.text
					if no_results == '':
						self.no_results_list.append({'keyword':key, 'hits': '0','text': 'No results for this query.'})
					else:
						p = re.compile(r'\s(\d+.\d+)+')
						no_results_number = p.search(no_results).group()
						removed_space = no_results_number.replace('\xa0', '')
						self.no_results_list.append({'keyword': key, 'hits':removed_space, 'text': no_results})
			for div in soup.find_all('div', class_='yuRUbf'):
				link = div.select('a', href=True)
				if link not in links_list:
					links_list.append(link[0]['href'])
				else:
					continue			
			time.sleep(delay)
		key_dict = {key:links_list}
		self.dict_list.append(key_dict)
		

	def main(self, pages, delay):
		self.open_keywords()
		for key in self.keywords:
			self.get_data(key, pages, delay)
		self.no_results_csv(self.no_results_list)
		self.links_csv(self.dict_list)

run = googleScrape(dict_list, no_results_list) 

if __name__ == '__main__':
	run.main(pages_to_scrape, delay)
