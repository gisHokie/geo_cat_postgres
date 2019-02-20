DATABASE_CONFIG = {
  "version": "1.0.0",
  "description": "list connections for different data servers",
  "Postgres": {
    "databases": [
      {
        "schema_name": "public",
        "database_name": "geo_cat",
        "user": "postgres",
		"pwd": "admin",
		"port": 4326,
		"host" : "localhost"
      },
      {
        "schema_name": "public",
        "database_name": "geo_cat_staging",
        "user": "postgres",
		"pwd": "admin",
		"port": 4326,
		"host" : "localhost"
      },
      {
        "schema_name": "public",
        "database_name": "geo_cat_data",
        "user": "postgres",
		"pwd": "admin",
		"port": 4326,
		"host" : "localhost"
      }   
    ]
  },
   "SQL_Server": {
    "databases": [
      {
        "schema_name": "",
        "database_name": "",
        "user": "",
		"pwd": "",
		"port": 1111,
		"host" : ""
      }
    ]
  }
}