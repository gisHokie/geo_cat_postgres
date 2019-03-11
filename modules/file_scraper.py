###################################
#author: Scott D. McDermott
#date: 12/15/2018
#summary:
###################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import NoSuchElementException

import requests, zipfile, io, os
import urllib
from pathlib import Path
import json
import re

class Scraper:

	def __init__(self):
		self.data = []
		
	def file_exist(self, file_path):
		bool_file = True
		get_file = Path(file_path)
		bool_file =  get_file.is_file()
		return bool_file
		
	# Create a year directory if it does not exist
	def create_dir_by_year(self, zip_path_year):
		if not os.path.exists(zip_path_year):
			os.makedirs(zip_path_year)
		
	# Create a Selenium Firefox driver to scrape the data from browser
	# Need to download the geckoDriverPath and save to known directory
	def get_firefox_driver_url(self, url_path, binary_path):
		binary = FirefoxBinary(binary_path)
		driver = webdriver.Firefox(firefox_binary=binary)
		driver.get(url_path)
		return driver

	# Loop through the HTML and read if only end point is *.SHP
	# Use XPATH to locate the HREF and file name path
	def get_text_by_attribute(self, t, attrib):
		getHrefValue = t.get_attribute(attrib)
		getTxtValue = t.text
		full_Href_Txt_Value = getHrefValue + ',' + getTxtValue
		return (full_Href_Txt_Value)

	# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
	def get_list_files_from_directory(self, dirName):
		# create a list of file and sub directories 
		# names in the given directory 
		listOfFile = os.listdir(dirName)
		allFiles = list()
		# Iterate over all the entries
		for entry in listOfFile:
			# Create full path
			fullPath = os.path.join(dirName, entry)
			# If entry is a directory then get the list of files in this directory 
			if os.path.isdir(fullPath):
				allFiles = allFiles + self.get_list_files_from_directory(fullPath)
			else:
				allFiles.append(fullPath)
					
		return (allFiles) 
		
	# Download zip file and save with name
	# Uncompress the Zip files and store in separate directory
	def extract_zipname_url(self, zip_path,zip_file_url):
		print('Extracting: ' + zip_file_url)
		r = requests.get(zip_file_url)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(zip_path)	

	def extract_zipname_path(self, zip_in_path, zip_out_path):
		z = zipfile.ZipFile(zip_in_path, 'r')
		z.extractall(zip_out_path)	
	
	# parses list of links to zip files in html page
	# to_find is a regex matching what you're searching for  
	def get_zip_list(self, get_request, to_find):
		# get html
		html = get_request.text
		# find zips
		matches = re.findall(to_find, html)

		return matches

	# strips unwanted strings from link
	def clean_zip_link(self, zip, strip_list):
		for i in strip_list:
			zip = zip.strip(i)
		return zip

	# stores shape files found in zip
	def write_files_from_zip(self, zip):
		files = zip.namelist()
		for i in files:
			if (re.match(r'.*\.shp', i) or re.match(r'.*\.shx', i) or re.match(r'.*\.dbf', i)) and not re.match(r'.*\.xml', i):
				print(i)
				print(zip.read(i))
		return 0

	def read_zip_file_content_values(self, filepath):
		zfile = zipfile.ZipFile(filepath)
		for finfo in zfile.infolist():
			ifile = zfile.open(finfo)
			line_list = ifile.readlines()
			return(line_list)
		
   # makes http get request to url
	def get_http_request(self, url):
		r = requests.get(url)
		if r.status_code != 200:
			sys.exit("the http request returned status code " + str(r.status_code))
		return r
		
#if __name__ == '__main__':

