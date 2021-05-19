
from bs4 import BeautifulSoup
import os
import requests
import json
import random

from adjectives import random_adjective

radar_base_url = 'https://www.thoughtworks.com/radar/'
quadrants = ['techniques', 'tools', 'platforms', 'languages-and-frameworks']
skill_items = {}

def skills(event, context):
    # Only update the list if empty
    if not skill_items:
        for quadrant in quadrants:
            target_radar_url = radar_base_url + quadrant
            target_radar_page = requests.get(target_radar_url)
            target_radar_soup = BeautifulSoup(target_radar_page.content, 'html.parser')
            target_radar = target_radar_soup.find(id='responsive-tech-radar')
            skill_items[quadrant] = skills_from_html(target_radar)
    
    phrase = get_phrase(skill_items)
    body = {
        'phrase': phrase,
        'jargon': generate_jargon(phrase)
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

def generate_jargon(phrase):
    return requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': phrase,
        },
        headers={'api-key': os.environ['DEEP_AI_TOKEN']}
    ).json()['output']

def get_phrase(skill_items):
    return 'I think that ' + random_skill(skill_items) + ' are ' + random_adjective() + ' and ' + random_skill(skill_items) + ' should strive to be more ' + random_adjective() + ' because'

def skills_from_html(html_target_radar):
    skill_group = {}
    options = ['adopt', 'trial', 'assess', 'hold']
    for option in options:
        radar_option = html_target_radar.find(id=option)
        items = radar_option.find_all('li')
        skill_group[option] = list(map(lambda x: x.find('a').text, items))
    return skill_group

def random_skill(skill_items):
    quadrants = ['techniques', 'tools', 'platforms', 'languages-and-frameworks']
    options = ['adopt', 'trial', 'assess', 'hold']
    choice = None
    while choice is None:
        quadrant = random.choice(quadrants)
        option = random.choice(options)
        try:
            choice = random.choice(skill_items[quadrant][option])
        except:
            print('hello i am a mediocre dev')
    return choice
