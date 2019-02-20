import shapefile
from json import dumps

# # variable stuff
# shape_Path = r'E:\dump\al142018_5day_021'
# shape_Name = 'al142018-021_5day_pgn.shp'
# geoJson_Path = r'E:\dump'
# geoJson_FileName = 'al142018_5day_021_pgn'

# shape_FullPath = shape_Path + r'\\' + shape_Name
# geoJson_FullPath = geoJson_Path + r'\\' + geoJson_FileName

# # read the shapefile
# reader = shapefile.Reader(shape_FullPath)
# fields = reader.fields[1:]
# field_names = [field[0] for field in fields]
# buffer = []

def get_feature_buffer(reader, field_names):
	buffer = []
	for sr in reader.shapeRecords():
		atr = dict(zip(field_names, sr.record))
		geom = sr.shape.__geo_interface__
		buffer.append(dict(type="Feature", \ 
		geometry=geom, properties=atr))
	return buffer
	
# write the GeoJSON file
def build_geojson(geoJson_FullPath, buffer)
	geojson = open(geoJson_FullPath, "w")
	geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
	geojson.close()