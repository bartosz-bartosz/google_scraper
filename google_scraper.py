import argparse
import requests
import urllib
import re
import csv
import time
import unicodedata
from bs4 import BeautifulSoup
from requests_html import HTMLSession

pages_to_scrape = 7 # How many result pages will be scraped
delay = 0 # How many seconds the program will wait before scraping next page (too fast scraping can lead to bad response from Google page)

'''Main program class'''
class googleScrape:
	def __init__(self):
		self.dict_list = []
		self.keywords = []
		self.total_results_list = []

	''' Open keywords.txt file, replace spaces with "+" for search purposes and store keywords in a list'''
	def open_keywords(self):
		with open('keywords.txt', 'r', encoding='utf8') as file:
			self.keywords = file.read().splitlines()
			self.keywords = [k.replace(' ', '+') for k in self.keywords]
		return self.keywords

	'''Reach a single page, check for response. If response is OK - return it and continue. Otherwise, save already collected data and close the program. '''
	def get_html(self, link):
		self.response = HTMLSession().get(link)
		print(self.response)
		if self.response.status_code == 200:
			print('Response OK, data reached successfully.\n')
			return self.response
		else:
			print("\nToo many tries. Saving data collected until now.\nTry again in a few minutes.If problem persists, set higher delay.\n")
			if len(self.total_results_list) < 1:
				print('\nNo data to save.')
				exit()
			else:
				self.total_results_csv(self.total_results_list)
				self.links_csv(self.dict_list)
				exit()

	'''Use BeautifulSoup module to transform the response from get_html() method into an iterable HTML'''
	def make_soup(self, url):
		self.response = self.get_html(self.URL)
		soup = BeautifulSoup(self.response.text, 'html.parser')
		return soup

	'''Save CSV file with total number of results for each keyword'''
	def total_results_csv(self, total_results_list):
		print('\n')
		total_results_file = 'total_results.csv'
		with open(total_results_file, 'w', newline='') as resultsfile:
			writer = csv.DictWriter(resultsfile, total_results_list[0].keys())
			writer.writeheader()
			writer.writerows(total_results_list)

		print(f'Number of results for each keyword saved to {total_results_file}')

	'''Save CSV file with all links with corresponding keyword'''
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

	'''Take keyword, create link in range of pages_to_scrape. Create URL for each page and pass it to make_soup() method. 
	Find total number of results and all links, save that data to lists of dictionaries and pass them to methods which create CSV files.
	If no results are found, put that information instead. If link already appears in results for the same keyword, ignore it.
	After scraping every page wait for time specified in "delay" variable.'''
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
					total_results = div.text
					if total_results == '':
						self.total_results_list.append({'keyword':key, 'hits': '0','text': 'No results for this query.'})
					else:
						p = re.compile(r'\s(\d+.\d+)+')
						total_results_number = p.search(total_results).group()
						removed_space = total_results_number.replace('\xa0', '')
						self.total_results_list.append({'keyword': key, 'hits':removed_space, 'text': total_results})
			for div in soup.find_all('div', class_='yuRUbf'):
				link = div.select('a', href=True)
				if link not in links_list:
					links_list.append(link[0]['href'])
				else:
					continue			
			time.sleep(delay)
		key_dict = {key:links_list}
		self.dict_list.append(key_dict)
		
	'''Main method. Read keywords, then iterate through them in get_data() method.'''
	def main(self, pages, delay):
		self.open_keywords()
		for key in self.keywords:
			self.get_data(key, pages, delay)
		if self.response.status_code == 200:
			self.total_results_csv(self.total_results_list)
			self.links_csv(self.dict_list)
		else:
			exit()

'''Create instance of a program'''
run = googleScrape() 

'''Run'''
if __name__ == '__main__':
	run.main(pages_to_scrape, delay)
