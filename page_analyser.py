import argparse
from bs4 import BeautifulSoup as bs
import numpy
import re
import requests
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import urlsplit


class PageAnalyser():
	def __init__(self, url):
		self.url = url
		self.parsed_page_content=None
		self.internal_links=[]
		self.include_url=['','.']
		self.links_and_anchor_texts=[]
		self.All_Internal_links={}
	def get_page_content(self):
		try:
			# Some sites do not allow requests without headers
			# The headers dictionary deals with this
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
			AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
			# requests.get only works with urls with http or https
			if re.match(r"(https://|http://).+", self.url):
				page_object = requests.get(self.url, headers=headers)
			else:
				page_object = requests.get("https://{}".format(self.url), headers=headers)
			page_content = page_object.content
			self.parsed_page_content = bs(page_content, "html.parser")
		except requests.exceptions.ConnectionError:
			print("Error: Something is wrong with the url")
		

	def get_links_and_anchor_texts(self):
		anchor_tags = self.parsed_page_content.find_all("a")
		links = []
		anchor_text = []
		for anchor_tag in anchor_tags:
			# Some anchor tags do not have href attributes
			# Use an empty string as the href value of such tags
			try:
				links.append(anchor_tag["href"])
			except KeyError:
				links.append("")
			anchor_text.append(anchor_tag.text.strip())
		self.links_and_anchor_texts = list(zip(links, anchor_text))
		#return links_and_anchor_texts

	def get_url_one_level_down(self,link):
		scheme=urlsplit(link).scheme
		netloc= urlsplit(link).netloc
		if((scheme =='')| (netloc=='')):
			return link
		base_url='://'.join([urlsplit(link).scheme,urlsplit(link).netloc])
		path=urlsplit(link).path
		path=path.split('/')
		one_level= [base_url,path[1]]
		return '/'.join(one_level)

	def get_internal_links(self):
		All_links=self.links_and_anchor_texts
		includeurl=urlparse(self.url).netloc
		if(All_links==[]):
			return 'Empty link was passed'
		else:
			for link in All_links:
				link_netloc=urlparse(link[0]).netloc
				if (link_netloc == includeurl)| (link_netloc in self.include_url):
					new_link=self.get_url_one_level_down(link[0])
					self.internal_links.append((new_link,link[1]))
				else:
					pass
			self.All_Internal_links={'internal_links':self.internal_links}
		

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", '--link', help='add a url to test', type=str)
	args = parser.parse_args()
	pageanalyser = PageAnalyser(args.link)
	pageanalyser.get_page_content()
	pageanalyser.get_links_and_anchor_texts()
	pageanalyser.get_internal_links()
	print(pageanalyser.All_Internal_links)


	
if __name__ == '__main__':
	main()