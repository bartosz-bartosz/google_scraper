import requests
import urllib
from bs4 import BeautifulSoup
# from requests_html import HTML
from requests_html import HTMLSession

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
# headers = {'user_agent': USER_AGENT}

keywords = []

class googleScrape:
	def __init__(self):
		self.keywords = []

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

	# def scrape_urls(self, query):
	# 	response = self.get_site(self.URL)
	# 	links = list(response.html.absolute_links)
	# 	return links

	def make_soup(self, query):
		response = self.get_html(self.URL)
		soup = BeautifulSoup(response.text, 'html.parser')
		for div in soup.find_all('div', class_='yuRUbf'):
			link = div.select('a', href=True)
			print(link[0]['href'])
			''' NEXT: LINKS TO BE SAVED IN A FILE'''
		for div in soup.find_all('div', class_='LHJvCe'):
			print(type(div.text))
			print(div.text)

	def main(self):
		self.open_keywords()
		#scrape_urls(URL)
		for k in self.keywords:
			self.URL = f"https://google.com/search?q=site:https://www.searchenginejournal.com/+{k}&start=1"
			self.make_soup(self.URL)

run = googleScrape() 

if __name__ == '__main__':
	run.main()
