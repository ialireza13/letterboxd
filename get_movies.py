import requests
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTMLSession
from tqdm import tqdm
from time import sleep

base_url = 'https://letterboxd.com/films/by/rating/size/small/page/'
page = 124

while(True):
    print("Page:",page)
    url = base_url+str(page)
    print(url)
    page+=1
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
    while(True):
        try:
            response.html.render()

            html = response.html.raw_html

            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find(id='content')
            content = content.find(class_='content-wrap')
            content = content.find(class_='section col-24 col-main')
            content = content.find(id='films-browser-list-container')
            content = content.find(class_='poster-list -p70 -grid')
            
            items = content.find_all(class_='listitem poster-container')
            items = [item.find_all(class_='')[0].find(class_='frame') for item in items]
        except:
            print('Error in rendering, retrying...')
            sleep(2)
            continue
        break

    names = []
    links = []
    years = []
    for i in tqdm(range(len(items))):
        attrs = items[i].attrs
        name_ = attrs['data-original-title'].split(sep=' ')
        names.append(' '.join(name_[:-1]))
        links.append('https://letterboxd.com'+attrs['href'][:-1])
        years.append(name_[-1][1:-1])
    
    with open('movies.txt','a') as f:
        for i in range(len(names)):
            f.writelines(names[i]+','+years[i]+','+links[i]+'\n')