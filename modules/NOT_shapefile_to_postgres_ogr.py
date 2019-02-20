###################################
#author: 
#date:
#summary:
# Go to directory where shp is located
# Read each sub folders
# Locate SHP, DBF, and SHX
# Get the Path and file name of the SHP
# Add SHP file name to CMD and Execute
# http://www.bostongis.com/pgsql2shp_shp2pgsql_quickguide.bqg
#
# Reference Links (Current and Future):
#https://gis.stackexchange.com/questions/258052/how-to-specify-a-password-with-shp2pgsql-using-centos
# https://gis.stackexchange.com/questions/90085/import-shp-to-postgis-using-python-and-ogr
# http://www.postgresqltutorial.com/postgresql-python/call-stored-procedures/
# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
# https://pynative.com/python-postgresql-tutorial/
###################################

import os
import subprocess
from os import listdir
from os.path import isfile, join

import psycopg2
# from config import config



def shp_to_postgres(cmd):
	# Execute command to post shapes to postgres
	subprocess.call(cmd, shell=True)

	


def insert_into_postgres(DATABASE_CONFIG):
	""" insert multiple vendors into the vendors table  """
	sql = "INSERT INTO source_geo(source_description, version_number, create_date) VALUES(%s%s%s)"
	conn = None

	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(DATABASE_CONFIG)
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.executemany(sql,source_descript, version_num, create_dt)
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def p_conn(dconfig):
	""" get parts provided by a vendor specified by the vendor_id """
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(
								user = dconfig['user'],
								password = dconfig['password'],
								host = dconfig['host'],
								port = dconfig['port'],
								dbname = dconfig['dbname']								
								)
	except (Exception, psycopg2.DatabaseError) as error:
			print(error)
	# finally:
		# if conn is not None:
			# conn.close()
	return(conn)
	
def call_sp_postgres(conn, sp_name, sp_values, s_percent):
	# create a cursor object for execution
	cur = conn.cursor()
	# another way to call a stored procedure
	build_call = "CALL " + sp_name + s_percent
	print(build_call)
	# Some tables do not allow dupe records for a field, this will capture any potential dupes and return a pass/fail string
	try: 
		cur.execute(build_call, (sp_values))  #.execution_options(autocommit=True)
		conn.commit()
	except:
		return 'failed'
	cur.close()
	return 'passed'
		
def exec_select_id(conn, sp_name, sp_values, s_percent):
	frow = ''
	cur = conn.cursor()
	get_value = '0'
	build_call = "SELECT " + sp_name + s_percent
	cur.execute(build_call, (sp_values))
	# # process the result set
	row = cur.fetchone()
	if row[0] is not None:
		frow = row[0]
	# close the communication with the PostgreSQL database server
	return frow