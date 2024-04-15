import requests
import json
from bs4 import BeautifulSoup as bs
import os.path

dict_of_ganres = {}

def create_dict_of_ganres():
    """The dictionary creation function is used to create a file with links to anime genres.
    This is required to avoid creating unnecessary requests to the site."""
    global dict_of_ganres
    if os.path.exists('ganres.txt'):
        dict_of_ganres = get_dict()
        return(dict_of_ganres)
    else:
        if not dict_of_ganres:
            responce_get = requests.get('https://animestars.org/aniserials/video/')
            print(responce_get.status_code)
            if responce_get.status_code == 200:
                soup = bs(responce_get.text, 'html.parser')
                quotes_ganres = soup.find('ul', class_='flex-row-cat')
                a_tags = quotes_ganres.find_all('a')
                for element in a_tags:
                    name = element.text
                    urls = element['href']
                    dict_of_ganres[name] = urls
            jsondict()
        return(dict_of_ganres)


def jsondict():
    """Function for writing a dictionary to a json file"""
    with open('ganres.txt', 'w') as file:
        json.dump(dict_of_ganres, file)


def get_dict():
    """Function for getting data from a json file"""
    if os.path.exists('ganres.txt'):
        with open('ganres.txt', 'r') as file:
            dict_of_ganres = json.load(file)
            return(dict_of_ganres)
    else:
        dict_of_ganres = create_dict_of_ganres()
        return (dict_of_ganres)


if __name__ == "__main__":
    """Test filling the dictionary file"""
    create_dict_of_ganres()
    print(get_dict())
    print(dict_of_ganres)
