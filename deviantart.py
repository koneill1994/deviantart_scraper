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
    tags=soup.find(attrs={"class":"dev-about-tags-cc dev-about-breadcrumb"}).find_all(attrs={"class":"discoverytag"})
    return [a.contents[1] for a in tags]

#<div class="dev-about-tags-cc dev-about-breadcrumb">

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

# print(GetTagsForUser("axsens"))

# a=GetUserFriends("nummypixels")
# print(len(a))

# print(GetUserFriends("lopoddity"))

# print(GetUserKeywords("aplexpony"))

# print(GetDeviationTags("https://www.deviantart.com/aplexpony/art/Three-faces-of-Rarity-783993670"))



def CreateNode(G,user):
    G.add_node(user,tags=GetTagsForUser(user))
    # add node returns None
    
    
    
def AddFriends(G,user,depth):
    for friend in GetUserFriends(user):
        print(friend)
        if friend not in G.nodes:
            CreateNode(G,friend)
            G.add_edge(user,friend)
            if(depth>0):
                AddFriends(G,user,depth-1)
        

# creating the graph

G=nx.Graph()

start="axsens"
CreateNode(G,start)

max_depth=2

AddFriends(G,start,max_depth)

nx.write_gpickle(G,"test.gpickle")

print("nodes: "+str(G.number_of_nodes()))
print("edges:"+str(G.number_of_edges()))


    