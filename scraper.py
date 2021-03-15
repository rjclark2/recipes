import requests
import os
from ediblepickle import checkpoint
import time
import urllib
import re
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import gzip
urldict = {'epi':'https://www.epicurious.com/recipes/member/views/'
        ,'2epi' : 'https://www.epicurious.com/recipes/food/views/'
        ,'yum':'https://www.yummly.com/recipe/'
        ,'bon':'https://www.bonappetit.com/recipe/'
        ,'ny':'https://cooking.nytimes.com/recipes/'
        ,'ar':'https://www.allrecipes.com/recipe/'
        ,'poy':'https://pinchofyum.com/'
        ,'fn':'https://www.foodnetwork.com/recipes/'}


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_urls():
    ny_geturl()
    ar_geturl()
    poy_geturl()
    bon_geturl()
    epi_geturl()
    yum_geturl()
    fn_geturl()

def download_htmls(name):
    if name == 'all':
        for i in urldict:
            download_htmls(i)
    else:
        with open('urls/'+name+'_urls','r') as r:
            numbers = r.readlines()
            numbers = [x.replace('\n','') for x in numbers]
            numbers_set = set(number.replace(urldict[name],'') for number in numbers)
        files = os.listdir('cache')
        files = set(f[len(name):-2] for f in files if f.startswith(name)) 
        print(len(numbers_set))
        print(len(files))
        numbers = list(numbers_set-files)
        print(len(numbers))
        numbers = [urldict[name]+x for x in numbers if len(x) < 250]
        chunked = list(chunks(numbers,5))
        print('Here we go...')
        for i in chunked:
            gethtmls(name,i)


@checkpoint(key= lambda args, kwargs: ''.join([args[1], (args[0].url).replace(args[2],''), '.p']).replace('/',''),work_dir='cache')
def get_techs(response,name,parent):
    print(response.url)
    if response.status_code != 200:
        return None
    return response.content

def gethtmls(name,numbers):
    urls = [x for x in numbers]
    session = FuturesSession()
    while True:
        try:
            futures = [session.get(url) for url in urls]
            techs = [get_techs(future.result(),name,urldict[name]) for future in futures]
        except:
            print('waiting...')
            print(urls)
            time.sleep(10)
            print('starting again...')
            continue
        break

@checkpoint(key= lambda args, kwargs: ''.join([args[0],args[1],'.p']).replace('/',''), work_dir='cache')
def gethtml(name,number):
    number = number.replace(urldict[name],'')
    try:
        result = requests.get(urldict[name]+number,headers={'type':'html','User-Agent':'Mozilla/5.0'})
    except:
        time.sleep(10)
        result = requests.get(urldict[name]+number,headers={'type':'html','User-Agent':'Mozilla/5.0'})
    print('wrote ' + result.url)
    return result.content



### CODE FOR NYTIMES COOKING DATA EXTRACTION ###

#obtain valid URLS

def yum_geturl():
    request = requests.get('https://www.yummly.com/yummly-pages-recipe-0.xml')
    soup = BeautifulSoup(request.text,'xml')
    urls = soup.find_all('loc')
    urls = [x.text for x in urls if '/recipe/' in x.text]
    with open('urls/yum_urls','w') as w:
        for i in urls:
            w.write(str(i) + '\n')

def epi_geturl():
    request = requests.get('https://www.epicurious.com/sitemap.xml/member-recipes')
    soup = BeautifulSoup(request.text,'xml')
    urls = soup.find_all('loc')
    urls = [x.text for x in urls]
    for i in urls:
        print(i)
        while True:
            try:
                request = requests.get(i)
            except:
                print('waiting....')
                time.sleep(10)
                continue
            soup = BeautifulSoup(request.text,'xml')
            text = soup.find_all('loc')
            text = [x.text for x in text if '/recipes/member/' in x.text]
            with open('urls/epi_urls','a') as w:
                for j in text:
                    w.write(str(j) + '\n')
            break
    request = requests.get('https://www.epicurious.com/sitemap.xml/editorial-recipes')
    soup = BeautifulSoup(request.text,'xml')
    urls = soup.find_all('loc')
    urls = [x.text for x in urls]
    for i in urls:
        print(i)
        while True:
            try:
                request = requests.get(i)
            except:
                print('waiting....')
                time.sleep(10)
                continue
            soup = BeautifulSoup(request.text,'xml')
            text = soup.find_all('loc')
            text = [x.text for x in text if '/recipes/' in x.text]
            with open('2epi_urls','a') as w:
                for j in text:
                    w.write(str(j) + '\n')
            break


def bon_geturl():
    request = requests.get('https://www.bonappetit.com/sitemap.xml')
    soup = BeautifulSoup(request.text,'xml')
    urls = soup.find_all('loc')
    urls = [x.text for x in urls]
    numbers = []
    for i in urls:
        print(i)
        request = requests.get(i)
        soup = BeautifulSoup(request.text,'xml')
        text = soup.find_all('loc')
        text = [x.text for x in text if '/recipe/' in x.text]
        numbers += text
    with open('urls/bon_urls','w') as w:
        for i in numbers:
            w.write(str(i) +'\n')


def fn_geturl():
    url = 'https://www.foodnetwork.com/sitemaps/sitemap_food_index.xml'
    html = urllib.request.urlopen(url).read()
    html = str(html)
    urls = re.findall('https://www.foodnetwork.com/sitemaps/sitemap_food_[0-9]*.xml.gz',html)
    numbers = []
    print(len(urls))
    for i in urls:
        print(i)
        url = i
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                html = uncompressed.read()
        html = str(html)
        numbert = re.findall('https://www.foodnetwork.com/recipes/([a-zA-Z0-9\-]*)',html)
        numbert = [x for x in numbert if 'photos' not in x and 'menus' not in x and 
                  'articles' not in x and 'packages' not in x]
        for j in numbert:
            numbers.append(j)
    numbers.sort()
    with open('urls/fn_urls','w') as w:
        for i in numbers:
            w.write(str(i) + '\n')
    print('Got FN URLS')

def ny_geturl():
    url = 'https://www.nytimes.com/sitemaps/new/cooking.xml.gz'
    html = urllib.request.urlopen(url).read()
    html = str(html)
    urls = re.findall('https://www.nytimes.com/sitemaps/new/cooking-[0-9\-]*.xml.gz',html)
    numbers = []
    print (len(urls))
    for i in urls:
        print(i)
        url = i
        html = urllib.request.urlopen(url).read()
        html = str(html)
        numbert = re.findall('https://cooking.nytimes.com/recipes/([0-9]*)', html)
        numbert = [int(x) for x in numbert]
        for j in numbert:
            numbers.append(j)
    numbers.sort()
    with open('urls/ny_urls','w') as w:
        for i in numbers:
            w.write(str(i) + '\n')
    print('Got NYTimes URLS')

###  CODE FOR ALLRECIPE COOKING DATA EXTRACTION  ###

#obtain valid URLS

def ar_geturl():
    url = 'https://www.allrecipes.com/sitemaps/recipe/1/sitemap.xml'
    url2 = 'https://www.allrecipes.com/sitemaps/recipe/2/sitemap.xml'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'xml')
    text = soup.get_text()
    html2 = urllib.request.urlopen(url2).read()
    soup2 = BeautifulSoup(html2,'xml')
    text2 = soup2.get_text()
    numbers = re.findall('recipe/([0-9]*)/',text)
    numbers2 = re.findall('recipe/([0-9]*)/',text2)
    numbers = [int(x) for x in numbers]
    numbers2 = [int(x) for x in numbers2]
    numberst = numbers + numbers2
    numberst.sort()
    with open('urls/ar_urls', 'w') as r:
        for i in numberst:
            r.write(str(i) +'\n')
    print('Got Allrecipe URLS')


#CODE FOR PINCH OF YUM COOKING DATA EXTRACTION

#obtain valid URLS

def poy_geturl():
    urls = ['https://pinchofyum.com/post-sitemap2.xml','https://pinchofyum.com/post-sitemap1.xml']
    number = []
    for i in urls:
        url = i
        html = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(html).read()
        html = str(html)
        numbers = re.findall('https://pinchofyum.com/([0-9a-zA-Z\-]*)<',html)
        for i in numbers:
            number.append(i)
    number.sort()
    with open('urls/poy_urls','w') as w:
        for i in number:
            w.write(str(i) + '\n')
    print('Got POY URLS')

if __name__ == "__main__":
    get_urls()
    download_htmls('all')
