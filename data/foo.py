import json

# Specify the path to your JSON file
json_file_path = './data/mhrice.json'

# Open the JSON file for reading
with open(json_file_path, 'r') as json_file:
    # Parse the JSON data from the file
    data = json.load(json_file)

# Now, 'data' contains the contents of the JSON file as a Python dictionary or list, depending on the JSON structure.

# for key in data.keys():
#     print(key)
#     # armor, overwear?, equip_skill, decorations, weapon_series_mr?, airou_armor?, hyakuryu_skill?

# for v in data['armor_series_name_msg_mr']:
#     print(v)
#     print()


# armor_head_name_msg_mr - for the names of all armor pieces and their id in their name

# Filter keys starting with 'armor'
filtered_data = {k: v for k, v in data.items() if k.startswith('armor')}

# Export the filtered data to a JSON file
with open('filtered_data.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)