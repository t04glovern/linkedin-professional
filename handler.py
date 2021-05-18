
from bs4 import BeautifulSoup
import requests

radar_base_url = 'https://www.thoughtworks.com/radar/'
quadrants = ['techniques', 'tools', 'platforms', 'languages-and-frameworks']

def skills(event, context):
    skill_items = {}
    for quadrant in quadrants:
        target_radar_url = radar_base_url + quadrant
        target_radar_page = requests.get(target_radar_url)
        target_radar_soup = BeautifulSoup(target_radar_page.content, 'html.parser')
        target_radar = target_radar_soup.find(id='responsive-tech-radar')
        skill_items[quadrant] = skills_from_html(target_radar)

    return {
        "statusCode": 200,
        "body": skill_items
    }

def skills_from_html(html_target_radar):
    skill_group = {}
    options = ['adopt', 'trial', 'assess', 'hold']
    for option in options:
        radar_option = html_target_radar.find(id=option)
        items = radar_option.find_all('li')
        skill_group[option] = list(map(lambda x: x.find('a').text, items))
    return skill_group
