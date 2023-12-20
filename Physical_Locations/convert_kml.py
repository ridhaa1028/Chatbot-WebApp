import kml2geojson

json_data_list = kml2geojson.convert('MainCampusGlassboro.kml')
data_dict = json_data_list[0]

    # Function to replace empty strings with 'None'
def get_value_or_none(key):
    value = properties.get(key, 'None')
    return 'None' if value == '' else value

for i in range(len(data_dict['features'])):
    properties = data_dict['features'][i]['properties']
    geometry = data_dict['features'][i]['geometry']

    name = get_value_or_none('name')
    description = get_value_or_none('description')
    keywords = get_value_or_none('Keywords')
    categories = get_value_or_none('Categories')
    latitude = geometry['coordinates'][1]
    longitude = geometry['coordinates'][0]

    print('name: ', name, "\n")
    print('description: ', description, "\n")
    print('keywords: ', keywords, "\n")
    print('categories: ', categories, "\n")
    print('lat: ', latitude, "\n")
    print('long: ', longitude, "\n")


#print(data_dict[what_we_need][9]['properties']['Location'])
#print(data_dict[what_we_need][9]['properties']['Location'])
#print(data_dict[what_we_need][9]['properties']['Location'])


# Notes
# kml2geojson.convert(kml_file) returns a list of one dict
# dict has two keys: type, features
# what we need is features whose values are a list