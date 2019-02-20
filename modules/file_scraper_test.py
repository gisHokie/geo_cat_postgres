import requests, re, zipfile, io

def main():
    #init vars
    url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=all4&year=2018'
    base_url = 'https://www.nhc.noaa.gov/gis/'
    to_find = re.compile(r'a href\=".*\.zip"')
      
    # get list of links to zip files
    zip_list = get_zip_list(url_path, to_find)
    
    # decide what to strip
    strip_list = ['a href=', '\"']
    cleaned_links = []
    
    # clean zip list
    for i in zip_list:
        tmp = clean_zip_link(i, strip_list)
        cleaned_links.append(tmp)
           
    # request data from zip urls and write files
    for i in cleaned_links:
        url = base_url + i
        r = get_http_request(url)
    
        myfile = zipfile.ZipFile(io.BytesIO(r.content))
        write_files_from_zip(myfile)
		
		
		# shp_path = myfile.read(i)
		# # # UNCOMMENT THIS WHEN READY TO POST TO POSTGRESPost the shapes to Postgres
		# cmd = 'shp2pgsql -s ' + str(port) + ' ' + shp_path + ' | psql -h ' + hostname +  ' -d ' + dbasename + ' -U ' + username + ' PGPASSWORD ' + pwd + ' -q'
		# stp.shp_to_postgres(cmd)
		
##https://gis.stackexchange.com/questions/60837/loading-shapefile-to-a-specific-table-in-postgis-using-ogr2ogr
## ogr2ogr -append -f "PostgreSQL" PG:"dbname=db" shapefile.shp -nln mytable 

            
# parses list of links to zip files in html page
# to_find is a regex matching what you're searching for  
def get_zip_list(url, to_find):
    # request url
    r = get_http_request(url)

    # get html
    html = r.text

    # find zips
    matches = re.findall(to_find, html)
    
    return matches

# strips unwanted strings from link
def clean_zip_link(zip, strip_list):
    for i in strip_list:
        zip = zip.strip(i)
    return zip

# stores shape files found in zip
def write_files_from_zip(zip):
    files = zip.namelist()
    for i in files:
        if (re.match(r'.*\.shp', i) or re.match(r'.*\.shx', i) or re.match(r'.*\.dbf', i)) and not re.match(r'.*\.xml', i):
            print(i)
            print(zip.read(i))
    return 0
   
# makes http get request to url
def get_http_request(url):
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit("the http request returned status code " + str(r.status_code))
    return r
    
if __name__== "__main__":
  main()