import json

# Specify the path to your JSON file
json_file_path = './data/mhrice.json'

# Open the JSON file for reading
with open(json_file_path, 'r') as json_file:
    # Parse the JSON data from the file
    data = json.load(json_file)

# list of stuff we want for now
# player_skill_name_msg(_mr) - names of skills and their ids
# hyakuryu_skill_name_msg(_mr) - names of rampage skills and their ids
# decorations and decorations_name_msg(_mr) - names and associated skills of decorations
# hyakuryu_decos and hyakuryu_decos_name_msg - names and associated rampage skills of rampage decos
# armor and armor_[body_part]_name_msg(_mr) - for names and stats of armor