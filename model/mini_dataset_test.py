import requests as re
from bs4 import BeautifulSoup
import os

URL = "https://www.kaggle.com"
response = re.get(URL)
folder = "./model/mini_dataset"
path = os.getcwd() + "/" + folder

if not os.path.exists(folder):
    os.mkdir(folder)
    
def scrape_content(URL):
    response = re.get(URL)
    
    if response.status_code == 200:
        print("Conexão HTTP realizada com sucesso para o URL: ", URL)
        return response
    else:
        print("Conexão HTTP falhou para o URL: ", URL)
        return None
    
def save_html(to_where, text, name):
    file_name = name + ".html"
    with open(os.path.join(to_where, file_name), "w", encoding="utf-8") as f:
        f.write(text)
        

URL_list = [
    "https://www.google.com",
    "https://www.kaggle.com",
    "https://stackoverflow.com",
    "https://www.researchgate.net",
    "https://www.python.org",
    "https://www.w3schools.com",
    "https://wwwen.uni.lu",
    "https://github.com",
    "https://scholar.google.com",
    "https://www.mendeley.com",
    "https://www.overleaf.com"
]

def create_mini_dataset(to_where, URL_list):
    for i in range(0, len(URL_list)):
        content = scrape_content(URL_list[i])
        if content is not None:
            save_html(to_where, content.text, str(i))
        else:
            pass
    print("Mini dataset criado")
    
create_mini_dataset(path, URL_list)