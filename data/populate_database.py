from main_app.models import Skill, Decoration, Armor, ArmorSkill
import json
import re
from collections import defaultdict

# Load JSON data
with open('data/filtered.json', 'r') as file:
    data = json.load(file)

# parse skill data
    
# skill names
skill_dic = defaultdict(dict)
keys = ['player_skill_name_msg', 'player_skill_name_msg_mr']
for k in keys:
    skill_list = data[k]['entries']
    for skill in skill_list:
        rematch = re.search(r'_(\d+)_', skill['name'])
        if not rematch:
            continue

        skill_id = int(rematch.group(1))
        skill_name = skill['content'][1]
        skill_dic[skill_id]['name'] = skill_name

# skill descriptions
keys = ['player_skill_explain_msg', 'player_skill_explain_msg_mr']
for k in keys:
    skill_list = data[k]['entries']
    for skill in skill_list:
        rematch = re.search(r'_(\d+)_', skill['name'])
        if not rematch:
            continue

        skill_id = int(rematch.group(1))
        skill_desc = skill['content'][1]
        skill_dic[skill_id]['description'] = skill_desc

# skill max levels
skill_list = data['equip_skill']['param']
for skill in skill_list:
    if 'Skill' in skill['id']:
        skill_id = skill['id']['Skill']
    else:
        skill_id = skill['id']['MrSkill'] + 200
    
    max_level = skill['max_level'] + 1
    skill_dic[skill_id]['max_level'] = max_level

#print(json.dumps(skill_dic, indent=4))
    



# parse decorations
# deco names
deco_dic = defaultdict(dict)
keys = ['decorations_name_msg', 'decorations_name_msg_mr']
for k in keys:
    deco_list = data[k]['entries']
    for deco in deco_list:
        rematch = re.search(r'_(\d+)_', deco['name'])
        if not rematch or rematch.group(1) == "200": # deco 200 is not a real deco for some reason
            continue

        deco_id = int(rematch.group(1))
        deco_name = deco['content'][1]
        deco_dic[deco_id]['name'] = deco_name

# parse deco skills
# deco skills
deco_list = data['decorations']['param']
for deco in deco_list:
    if 'Deco' in deco['id']:
        deco_id = deco['id']['Deco']
    else:
        deco_id = deco['id']['MrDeco'] + 200
    
    skill = deco['skill_id_list'][0]
    if 'Skill' in skill:
        skill_id = skill['Skill']
    else:
        skill_id = skill['MrSkill'] + 200
    
    skill_level = deco['skill_lv_list'][0]
    size = deco['decoration_lv']

    deco_dic[deco_id]['skill_id'] = skill_id
    deco_dic[deco_id]['skill_level'] = skill_level
    deco_dic[deco_id]['size'] = size





# parse armor
# armor names
armor_dic = defaultdict(dict)
keys = [key for key in data.keys() if re.match(r'^armor_.+_name_msg', key)]
for k in keys:
    armor_list = data[k]['entries']
    for armor in armor_list:
        rematch = re.search(r'_(\d+)_', armor['name'])
        if not rematch: # deco 200 is not a real deco for some reason
            continue

        armorset_id = int(rematch.group(1))
        category = k.split('_')[1]
        armor_name = armor['content'][1]

        
        if category not in armor_dic[armorset_id]:
            armor_dic[armorset_id][category] = {}
        armor_dic[armorset_id][category]['armor_name'] = armor_name



# armor stats
armor_list = data['armor']['param']
for armor in armor_list:
    category = list(armor['pl_armor_id'].keys())[0].lower()
    armorset_id = armor['series']

    # deco slots
    deco_slots = [0, 0, 0]
    idx = 0
    deco_num_list = armor['decorations_num_list']
    for i, num_decos in enumerate(deco_num_list):
        for n in range(deco_num_list[i]):
            deco_slots[idx] = i
            idx += 1
    deco_slots.sort(reverse=True)
    armor_dic[armorset_id][category]['deco_slots'] = deco_slots

    # defenses
    armor_dic[armorset_id][category]['defense'] = armor['def_val']
    armor_dic[armorset_id][category]['fire'] = armor['fire_reg_val']
    armor_dic[armorset_id][category]['water'] = armor['water_reg_val']
    armor_dic[armorset_id][category]['thunder'] = armor['thunder_reg_val']
    armor_dic[armorset_id][category]['ice'] = armor['ice_reg_val']
    armor_dic[armorset_id][category]['dragon'] = armor['dragon_reg_val']

    # skills
    skill_ids = []
    for skill in armor['skill_list']:
        if skill == "None":
            break # this shouldn't be a problem as long as no skills come after a None
        
        if 'Skill' in skill:
            skill_ids.append(skill['Skill'])
        else:
            skill_ids.append(skill['MrSkill'] + 200)
    
    skill_levels = [lv for lv in armor['skill_lv_list'] if lv != 0]

    # handle some wonky stuff
    if len(skill_ids) > len(skill_levels):
        print("Error: More skill ids than levels")
        print(armorset_id)
        print(armor['skill_list'])
        print(armor['skill_lv_list'])
        break
    while len(skill_ids) < len(skill_levels):
        # this happens for a few armorsets, not sure why
        skill_levels.pop()

    armor_dic[armorset_id][category]['skill_ids'] = skill_ids
    armor_dic[armorset_id][category]['skill_levels'] = skill_levels
        

print(json.dumps(armor_dic, indent=4))