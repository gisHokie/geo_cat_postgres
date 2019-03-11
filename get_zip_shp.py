import requests, re, zipfile, io, sys, os, urllib, shutil
import modules.shapefile_to_postgres as stp
import modules.file_scraper as fsp

url_path = 'https://www.nhc.noaa.gov/gis/'
#'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=all4&year=2018'
base_url = 'https://www.nhc.noaa.gov'
in_data = './in_data'
zip_name_list = []
url_zip_regex = r'a href\=".*\.zip"'
strip_list = ['a href=', '\"']

scraper = fsp.Scraper()

# get list of links to zip files
get_req = scraper.get_http_request(url_path)
zip_list = scraper.get_zip_list(get_req, url_zip_regex)

cleaned_links = []
# clean zip list
for zl in zip_list:
	tmp = scraper.clean_zip_link(zl, strip_list)
	cleaned_links.append(tmp)

# request data from zip urls
for i in cleaned_links:
	url = base_url + i
	split_url = url.split('/')
	len_split_url = len(split_url)
	zip_name = split_url[len_split_url -1]
	zip_name_list.append(zip_name)

for znl in zip_name_list:
	full_zip_path = os.path.join(in_data,znl)
	with urllib.request.urlopen(url) as response, open(full_zip_path, 'wb') as out_file:
		print('Saving to local drive: ' + full_zip_path)
		data = response.read() # a `bytes` object
		out_file.write(data)