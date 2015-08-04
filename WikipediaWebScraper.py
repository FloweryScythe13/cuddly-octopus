from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import NavigableString
import urllib.request
import csv

BASE_URL = "https://en.wikipedia.org/wiki/"



def get_art(article_url):
    html = urllib.request.urlopen(article_url).read()
    soup = BeautifulSoup(html, "lxml")
    arttext = soup.find(id="mw-content-text", class_="mw-content-ltr")
    return arttext

def get_intro(arttext):
    intro_tag = []
    #print(arttext.find('div', id='toc'))
    #arttext.find('p', string=False)
    for p in arttext.find_all('p', recursive=False, limit = 6):
            
        for child in p.find_all(['a', 'b', 'span'], recursive=False):

            child.unwrap()

        if (p.next_sibling.next_sibling == arttext.find('div', id='toc')):

            break
        
        intro_tag.append(p.get_text() + '\n')

    

    return intro_tag

def get_toc(arttext):
    toc_raw = arttext.find('div', id='toc')
    toc_raw.h2.parent.clear()
        
    toc_stripped = toc_raw.get_text()
    
    return toc_stripped
    

wikiurl = input("Please specify the article URL for the desired Wikipedia entry: ")
soup = get_art(BASE_URL + wikiurl)
title = soup.b.get_text()
result = get_intro(soup)
print(title)
print(result)
toc_result = get_toc(soup)
print(toc_result)

"""
Here we will be using Tablib to create a Dataset object and pass our text data into it.
Then we will simply export that Dataset object into our xlsx spreadsheet.
"""

##data = tablib.Dataset(title, header='Article Name')
##data.append_col(toc_result, header='Table of Contents')
##data.append_col(result, header='Introductary Summary')
with open('scrapedoutput.csv', 'a', newline='') as f:
    outputWriter = csv.writer(f)
    outputWriter.writerow([title, toc_result, result])


