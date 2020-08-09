import requests
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTMLSession
from tqdm import tqdm
from time import sleep
from os.path import isfile

batch_size = 1
base_url = 'https://letterboxd.com/films/by/rating/size/small/page/'

if isfile('page_number.txt'):
    with open('page_number.txt', 'r+') as f:
        try:
            page = int(f.readline())
        except:
            page = 1
            f.write(str(page))
else:
    page = 1
    with open('page_number.txt', 'w') as f:
        f.write(str(page))

session = HTMLSession()

while(True):
    print("Page:",page)
    url = base_url+str(page)
    print(url)
    page+=1
    try:
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
            sleep(1)
            continue
        break

    names = []
    years = []
    links = []
    directors = []
    fans = []
    ratings = []
    watches = []
    durations = []
    likes = []
    for i in range(len(items)):
        
        attrs = items[i].attrs
        name_ = attrs['data-original-title'].split(sep=' ')
        names.append(' '.join(name_[:-1]))
        links.append('https://letterboxd.com'+attrs['href'][:-1])
        years.append(name_[-1][1:-1])
        
        while(True):
            try:
                response = session.get(links[-1])
                response.html.render()
                print(i)
                html = response.html.raw_html
                
                print(names[-1])
                soup = BeautifulSoup(html, 'html.parser')
                content = soup.find(id='content')
                content = content.find(class_='content-wrap')
                content = content.find(id='film-page-wrapper')
                stats = content.find(id='js-poster-col')
                content = content.find(class_='col-17')
                try:
                    duration_ = content.find(class_='text-link text-footer').text.split(sep=' ')[0]
                except:
                    duration_ = "null"
                
                director_ = content.find(id='featured-film-header')
                try:
                    director_ = director_.find_all(class_='prettify')[1].text
                except:
                   director_ = "null"

                content = content.find(class_='sidebar')
                content = content.find(class_='section ratings-histogram-chart')

                try:
                    fans_ = content.find(class_='all-link more-link').text.split(sep=' ')[0]
                except:
                    fans_ = "null"
                
                try:
                    ratings_ = content.find_all(class_='ir tooltip')
                    ratings_ = [rate.attrs['data-original-title'].split('\xa0')[0] for rate in ratings_]
                except:
                    ratings_ = ['','','','','','','','','','']               

                stats = stats.find(class_="poster-list -p230 no-hover el col")
                stats = stats.find(class_="film-stats")
                try:
                    watches_ = stats.find(class_='stat filmstat-watches').text
                except:
                    watches_ = "null"
                try:
                    likes_ = stats.find(class_='stat filmstat-likes').text
                except:
                    likes_ = 'null'
            except:
                print('Error in rendering, retrying...')
                sleep(1)
                continue
            break
        durations.append(duration_)
        directors.append(director_)
        fans.append(fans_)
        watches.append(watches_)
        likes.append(likes_)
        ratings.append(ratings_)

    if (page%batch_size==0):
        with open('movies-'+str(int(page/batch_size)+1)+'.txt','w') as f:
            for i in range(len(names)):
                f.writelines(names[i]+','+years[i]+','+links[i]+','+directors[i]+','+durations[i]+','+fans[i]+','+\
                    watches[i]+','+likes[i]+','+ratings[i][0]+'|'+ratings[i][1]+'|'+rating[i][2]+\
                    '|'+ratings[i][3]+'|'+ratings[i][4]+'|'+ratings[i][5]+'|'+ratings[i][6]+'|'+\
                    ratings[i][7]+'|'+ratings[i][8]+'|'+ratings[i][9]+'\n')
    else:
        with open('movies-'+str(int(page/batch_size)+1)+'.txt','a') as f:
            for i in range(len(names)):
                f.writelines(names[i]+','+years[i]+','+links[i]+','+directors[i]+','+durations[i]+','+fans[i]+','+\
                    watches[i]+','+likes[i]+','+ratings[i][0]+'|'+ratings[i][1]+'|'+rating[i][2]+\
                    '|'+ratings[i][3]+'|'+ratings[i][4]+'|'+ratings[i][5]+'|'+ratings[i][6]+'|'+\
                    ratings[i][7]+'|'+ratings[i][8]+'|'+ratings[i][9]+'\n')
    with open('page_number.txt', 'w') as f:
        f.write(str(page))