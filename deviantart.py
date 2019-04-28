import requests
from bs4 import BeautifulSoup
import networkx as nx
from itertools import chain
from collections import Counter

def GetUserKeywords(user):
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user).text,
        'html.parser'
    )
    return soup.find_all('meta',attrs={"name":"keywords"})[0]['content'].split(", ")


def GetUserFriendsPage(user,count):
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user+"/modals/myfriends/?offset="+str(count)).text,
        'html.parser'
    )
    return [a['title'] for a in soup.find_all(attrs={"class":"avatar"})]

def GetUserFriends(user):
    out=[]
    count=0
    while(True):
        k=GetUserFriendsPage(user,count)
        if(len(k)==0):
            break
        out=out+k
        count=count+100
    return out
        

def GetDeviationTags(url):
    soup=BeautifulSoup(
        requests.get(url).text,
        'html.parser'
    )
    return [a.contents[1] for a in soup.find_all(attrs={"class":"discoverytag"})]

def GetDeviations(user):
    # will only grab the first 24, more requires ajax requests which is a pain
    soup=BeautifulSoup(
        requests.get("https://www.deviantart.com/"+user+"/gallery/?catpath=/").text,
        'html.parser'
    )
    return [a['href'] for a in soup.find_all(attrs={"class":"torpedo-thumb-link"})]

def GetTagsForUser(user):
    return Counter(list(chain(*[GetDeviationTags(url) for url in GetDeviations(user)])))

# use tag similarity as distance metric?




# print(GetDeviationTags("https://www.deviantart.com/0-2-100/art/CLOSED-Lowblood-Troll-Adopts-Offer-To-Adopt-728467431"))

print(GetTagsForUser("axsens"))

# a=GetUserFriends("nummypixels")
# print(len(a))

# print(GetUserFriends("lopoddity"))

# print(GetUserKeywords("aplexpony"))

# print(GetDeviationTags("https://www.deviantart.com/aplexpony/art/Three-faces-of-Rarity-783993670"))