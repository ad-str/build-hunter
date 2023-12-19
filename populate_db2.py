from collections import defaultdict
import re
import json
from main_app.models import Skill, Decoration, Armor, ArmorSkill
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'build_hunter.settings')
django.setup()


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


if __name__ == "__main__":
    data = load_data('data/filtered.json')
    # skill_dic = extract_skills(data)
    # save_skill_objects(skill_dic)
    # print(Skill.objects.count())

    # deco_dic = extract_decorations(data)
    # save_deco_objects(deco_dic)
    # print(Decoration.objects.count())
