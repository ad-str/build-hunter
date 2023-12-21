import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'build_hunter.settings')
django.setup()

from collections import defaultdict
import re
import json
from main_app.models import Skill, Decoration, Armor, ArmorSkill

# Load JSON data

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def extract_skills(data):

    # helper function for extracting name and description
    def extract_string_info(key):
        for skill in data[key]['entries']:
            rematch = re.search(r'_(\d+)_', skill['name'])
            if rematch:
                skill_id = int(rematch.group(1))
                yield skill_id, skill['content'][1]

    # initialize output
    skill_dic = defaultdict(dict)

    # parse skill name
    for key in ['player_skill_name_msg', 'player_skill_name_msg_mr']:
        for skill_id, skill_name in extract_string_info(key):
            skill_dic[skill_id]['name'] = skill_name

    # parse skill description
    for key in ['player_skill_explain_msg', 'player_skill_explain_msg_mr']:
        for skill_id, skill_desc in extract_string_info(key):
            skill_dic[skill_id]['description'] = skill_desc

    # parse skill stats
    for skill in data['equip_skill']['param']:
        skill_id = skill['id'].get(
            'Skill', skill['id'].get('MrSkill', 0) + 200)
        max_level = skill['max_level'] + 1
        skill_dic[skill_id]['max_level'] = max_level

    return skill_dic


def save_skill_objects(skill_dic):
    new_skills = [Skill(id=id, **skill) for id, skill in skill_dic.items()]
    Skill.objects.bulk_create(new_skills)


def extract_decorations(data):
    def extract_deco_info(key):
        for deco in data[key]['entries']:
            rematch = re.search(r'_(\d+)_', deco['name'])
            if rematch:
                deco_id = int(rematch.group(1))
                yield deco_id, deco['content'][1]

    deco_dic = defaultdict(dict)
    for key in ['decorations_name_msg', 'decorations_name_msg_mr']:
        for deco_id, deco_name in extract_deco_info(key):
            deco_dic[deco_id]['name'] = deco_name

    for deco in data['decorations']['param']:
        deco_id = deco['id'].get('Deco', deco['id'].get('MrDeco', 0) + 200)
        skill_id = deco['skill_id_list'][0].get(
            'Skill', deco['skill_id_list'][0].get('MrSkill', 0) + 200)
        deco_dic[deco_id].update({
            'skill_id': skill_id,
            'skill_level': deco['skill_lv_list'][0],
            'size': deco['decoration_lv']
        })

    return deco_dic


def save_deco_objects(deco_dic):
    new_decos = []
    for id, deco in deco_dic.items():
        if 'skill_id' not in deco:
            continue
        skill = Skill.objects.get(id=deco['skill_id'])
        new_deco = Decoration(
            id=id, name=deco['name'], size=deco['size'], skill=skill, skill_level=deco['skill_level'])
        new_decos.append(new_deco)
    Decoration.objects.bulk_create(new_decos)


def extract_armors(data):
    # initialize output
    armor_dic = defaultdict(dict)

    # armor names
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
            armor_dic[armorset_id][category]['name'] = armor_name

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
            print("Error: More skill ids than levels", armorset_id)
            break
        while len(skill_ids) < len(skill_levels):
            # this happens for a few armorsets, not sure why
            skill_levels.pop()

        armor_dic[armorset_id][category]['skill_ids'] = skill_ids
        armor_dic[armorset_id][category]['skill_levels'] = skill_levels

    return armor_dic


def save_armor_objects(armor_dic):
    new_armors = []
    for armorset_id in armor_dic.keys():
        for category, armor in armor_dic[armorset_id].items():
            if 'defense' not in armor:
                continue

            new_armor = Armor(
                armorset_id=armorset_id,
                category=category,
                name=armor['name'],
                slot1=armor['deco_slots'][0],
                slot2=armor['deco_slots'][1],
                slot3=armor['deco_slots'][2],
                defense=armor['defense'],
                fire_res=armor['fire'],
                water_res=armor['water'],
                thunder_res=armor['thunder'],
                ice_res=armor['ice'],
                dragon_res=armor['dragon']
            )
            new_armors.append(new_armor)
    
    Armor.objects.bulk_create(new_armors)


def save_armorskill_objects(armor_dic):
    new_armor_skills = []
    for armorset_id in armor_dic.keys():
        for category, armor in armor_dic[armorset_id].items():
            if 'skill_ids' not in armor:
                continue

            armorObj = Armor.objects.get(armorset_id=armorset_id, category=category)
            for skill_id, skill_level in zip(armor['skill_ids'], armor['skill_levels']):
                skill = Skill.objects.get(id=skill_id)
                new_armor_skill = ArmorSkill(
                    armor=armorObj,
                    skill=skill,
                    level=skill_level
                )
                new_armor_skills.append(new_armor_skill)
    ArmorSkill.objects.bulk_create(new_armor_skills)


if __name__ == "__main__":
    data = load_data('data/filtered.json')
    # skill_dic = extract_skills(data)
    # save_skill_objects(skill_dic)
    # print(Skill.objects.count())

    # deco_dic = extract_decorations(data)
    # save_deco_objects(deco_dic)
    # print(Decoration.objects.count())

    # armor_dic = extract_armors(data)
    # save_armorskill_objects(armor_dic)
    # print(Armor.objects.count())
    # print(ArmorSkill.objects.count())
