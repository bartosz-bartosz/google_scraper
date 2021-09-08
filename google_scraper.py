import requests
import urllib
import csv
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

keywords = []
dict_list = []
no_results_list = []
pages_to_scrape = 5

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
			print("Too many tries. Saving data collected until now.")
			if self.no_results_list == []:
				print('No data to save.')
			else:
				self.no_results_csv(self.no_results_list)
				self.links_csv(self.dict_list)
 
	def make_soup(self, url):
		response = self.get_html(self.URL)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def no_results_csv(self, no_results_list):
		print('\n')
		# print('Number of results for all keywords:')
		print(no_results_list)
		no_results_file = 'no_results.csv'
		with open(no_results_file, 'w', newline='') as resultsfile:
			writer = csv.writer(resultsfile)
			for dic in no_results_list:
				writer.writerows(dic.items())
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

	def get_data(self, key, pages):
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
						self.no_results_list.append({key:'No results for this query.'})
					else:
						self.no_results_list.append({key:no_results})
					#print(f'{key}: {no_results}')
			for div in soup.find_all('div', class_='yuRUbf'):
				link = div.select('a', href=True)
				links_list.append(link[0]['href'])
				#print(links_list)				

		key_dict = {key:links_list}
		self.dict_list.append(key_dict)
		#print(dict_list)

	def main(self, pages):
		self.open_keywords()
		for key in self.keywords:
			self.get_data(key, pages)
		self.no_results_csv(self.no_results_list)
		self.links_csv(self.dict_list)

run = googleScrape(dict_list, no_results_list) 

if __name__ == '__main__':
	run.main(pages_to_scrape)
