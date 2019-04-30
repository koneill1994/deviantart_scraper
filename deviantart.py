import requests
from bs4 import BeautifulSoup
import networkx as nx
from itertools import chain
from collections import Counter, deque
import time
import matplotlib.pyplot as plt
import pickle

start_time=time.clock()

def ProgTime():
    return "["+str(time.clock()-start_time)+"s] "

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
    print(ProgTime()+"getting deviation tags for "+url)
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
    return dict(Counter(list(chain(*[GetDeviationTags(url) for url in GetDeviations(user)]))))

# use tag similarity as distance metric?




# print(GetDeviationTags("https://www.deviantart.com/0-2-100/art/CLOSED-Lowblood-Troll-Adopts-Offer-To-Adopt-728467431"))

# a=GetTagsForUser("axsens")

# print(a)
# print(type(a))

# a=GetUserFriends("nummypixels")
# print(len(a))

# print(GetUserFriends("lopoddity"))

# print(GetUserKeywords("aplexpony"))

# print(GetDeviationTags("https://www.deviantart.com/aplexpony/art/Three-faces-of-Rarity-783993670"))



def CreateNode(G,user):
    print(ProgTime()+"creating node "+user)
    G.add_node(user,tags=GetTagsForUser(user),checked=False)
    # add node returns None
    
    
# this is recursive and will eat up memory
# use the while loop below instead
def AddFriends(G,user,depth):
    SaveGraph(G)
    for friend in GetUserFriends(user):
        print(ProgTime()+friend)
        if friend not in G.nodes:
            CreateNode(G,friend)
            G.add_edge(user,friend)
            if(depth>0):
                AddFriends(G,user,depth-1)
        
def WriteJson(G,loc):
    f=open(loc,"w")
    f.write(string(nx.node_link_data(G)))
    f.close()

def DrawGraph(G):
  nx.draw(G)
  plt.show()

def SaveGraph(G):
    # nx.write_gpickle(G,"test.gpickle")
    nx.write_gexf(G, "test.gexf")
  
# creating the graph

fromscratch=True

if(fromscratch):
    G=nx.Graph()
    print(ProgTime()+"created graph")

    start="thekenzai1987"

    print(ProgTime()+"creating initial node")
    CreateNode(G,start)
    current=start 
    
else:
    G=nx.read_gexf("test.gexf")
    # uq=pickle.load( open( "user_queue.", "rb" ) )
    
# [print(G.nodes[a]) for a in G.nodes]
    
while any([not G.nodes[a]['checked'] for a in G.nodes]):

    for friend in GetUserFriends(current):
        if (friend not in G.nodes):
            CreateNode(G,friend)
            G.add_edge(current,friend)
        
    current['checked']=True

    current = next(i for i in G.nodes if not(G.nodes[i]['checked']))
    
    # pickle.dump(uq, open( "user_queue.p", "wb" ))
    SaveGraph(G)
    print(ProgTime()+"nodes: "+str(G.number_of_nodes()))
    print(ProgTime()+"edges:"+str(G.number_of_edges()))
    # print(ProgTime()+"queue length:"+str(len(uq)))
    

# G=nx.read_gexf("test.gexf")

# DrawGraph(G)


# uq (user queue) is a queue
# with elements representing
# el[0] : the user to be added
# el[1] : the user who this is a friend of, should be linked to

# algorithm:

# pop an el off the end of uq
# create a node off of el[0]
# if len(el[1])>0: make an edge between el[0] and el[1]

# look up each friend of el[0]
# if friend is not already a node or in uq
# add to uq [el[0],el[1]]

# ^ changes to friend search
# if we've added all of someone's friends

# any([not a['checked'] for a in G.nodes])

# save active state


# problem: the uq gets too massive to save in a pickle

# solution: 
# set an attribute to all nodes called "checked"
# which determines whether we've added all of that person's friends to the graph
# all values are initialized as false
# if we've added all of them we set it to true



# while any([not a['checked'] for a in G.nodes]):

# for each friend of current, add them as a node

# for friend in GetUserFriends(current):
    # if (friend not in G.nodes):
        # CreateNode(G,friend)
        # G.add_edge(current,friend)
        
# current['checked']=True

# current = next(i for i in G.nodes if not(i['checked'])



