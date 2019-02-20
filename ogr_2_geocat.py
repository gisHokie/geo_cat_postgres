#summary: Add compressed shapefiles to postgresql
###################################

import shutil, os
import json
import datetime
#import ogr2ogr

#Custom modules
import modules.file_scraper as fs
import modules.shapefile_to_postgres as stp
import zipfile
import re

dserver = 'Postgres'
zip_dir = ''
zip_out_dir =  ''
port = ''
hostname = '' 
username = '' 
pwd = '' 
hostname = ''
username = ''
pwd = ''
zip_bkup_dir = ''
shp_names = []
dbase_conn = {}
value_param = []
file_list = []
shp_list = []
shp_path_list = []
zip_out_dir_list=[]
feat_json = ''
data_json = ''
reg = r'.*\.shp($)'
# Get the current date and time in UTC format
get_datetime = datetime.datetime.utcnow()

# Get the basic info for each data obtained
json_config =  '.\\config\\config_features.json' 
json_config_data = '.\\config\\config_dbase.json'  
with open(json_config) as f:
	feat_json = json.load(f)
	
zip_bkup_dir = feat_json["properties"]['backup_data']
# Create the out_data and backup_data if it does not exists
# Assumption is that the in data exist because the user or automation has to store the data somewhere
if not os.path.exists(zip_bkup_dir):
	os.makedirs(zip_bkup_dir)
	
# Get the geo_cat_data database info
with open(json_config_data) as f:
	data_json = json.load(f)
# Get connection data directly from config file
port = data_json['Postgres']['databases'][0]['port']
hostname = data_json['Postgres']['databases'][0]['host']
username = data_json['Postgres']['databases'][0]['user']
pwd = data_json['Postgres']['databases'][0]['pwd']
dbasename = data_json['Postgres']['databases'][0]['database_name']
schemaname = data_json['Postgres']['databases'][0]['schema_name']

dbase_conn = {
'host': hostname,
'dbname': dbasename,
'user': username,
'password': pwd,
'port': port
}

# Instantiate the scaper class
spr = fs.Scraper()

# Read shapefiles directly from zip files
conn = stp.p_conn(dbase_conn)

# Read the reference table from postgres
get_obj_flds = []
get_obj_flds = stp.call_fx_postgres_many_rows(conn, 'geo_live.fx_get_geo_object_fields()','','')
for t in get_obj_flds:
	url = t[0]
	out_data = t[1]
	in_data = t[4]
	zip_name = t[2]
	feat_shp_name = t[3]
	fieldmap = t[5]
	url_id = t[6]
	feat_type_id = t[7]
	geom_type_id = t[8]

	# # Get zip files containing shapes
	# # Create a list all files in the directories and sub directories
	shp_full_path = os.path.join(out_data, feat_shp_name)
	zip_file = os.path.join(in_data,zip_name)
	
	# https://txt2re.com/index-python.php3?s=tl_2017_us_county.shp&-7&6
	# https://regex101.com/r/nMfmPs/1/
	if os.path.isfile(zip_file) :
		z = zipfile.ZipFile(zip_file)
		for filename in z.namelist():
			if re.search(reg, filename):
				# Add shapes to known direcotry
				just_shp_name = filename.replace('.shp','')
				just_zip_name = zip_name.replace('.zip','')
				#save the full path of shape file
				if not os.path.exists(out_data):
					os.makedirs(out_data)
				spr.extract_zipname_path(zip_file,out_data)

				print("Upsizing to Postgres: " + filename)
				# Make sure table has user privileges and schema name part of table
				cmd = 'D:\\OSGeo4W64\\bin\\ogr2ogr -update -append -fieldmap  '+ fieldmap + ' -a_srs EPSG:4326 -nlt GEOMETRY -lco "SCHEMA=geo_live" -f "PostgreSQL" PG:"host=' + hostname + ' user=' + 'postgres' + ' dbname=' + dbasename + ' password=' + pwd + '"  -skipfailures -nln geo_live.stg_geo_object_template '  + shp_full_path 
				#print(cmd)
				#stp.shp_to_postgres(cmd)

				# Get the names from geo_object_feature_type and source_geo source_geo_url and add to
				per_s = '(%s,%s,%s);'
				fx_value_list = []
				fx_value_list = (feat_type_id, geom_type_id, url_id)
				#update_geo_object_table = stp.call_sp_postgres(conn, 'geo_live.sp_geo_object_fk', fx_value_list, per_s)


#closing database connection.  Need to close it to allow the next INSERT
if(conn):
	conn.close()

# Move the Zip files to a new location
zip_dir = '.\in_data'
# files = os.listdir(zip_dir)
# for f in files:
	# try:
		# file_full_path = os.path.join(zip_dir, f)
		# shutil.move(file_full_path, zip_bkup_dir)
	# except Exception as e:
		# print(e)

# Delete the shape files
zip_out_dir = '.\out_data'
for the_dir in os.listdir(zip_out_dir):
	the_dir_path = os.path.join(zip_out_dir,the_dir)
	shutil.rmtree(the_dir_path) 